import datetime
import uuid
from datetime import timedelta

from fastapi import HTTPException, status

from src.auth import utils
from src.auth.redis import add_token_to_blacklist, is_token_blacklisted
from src.aws import utils as aws_utils
from src.rabbitmq import producer
from src.repositories.user_repository import UserRepository
from src.user.models import User


class AuthService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def create_new_user(self, request) -> User:
        if await self.user_repository.verify_user_exist(email=request.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )
        new_user = await self.user_repository.create_user(request)
        return new_user

    async def authenticate_user(self, form_data) -> dict:
        user = await self.user_repository.get_user_by_credentials(
            username=form_data.username, password=form_data.password
        )
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
            )
        user_id = str(user.id)
        access_token = utils.create_token(
            data={
                "user_id": user_id,
                "group_id": user.group_id,
                "username": user.username,
                "role": user.role.value,
            },
            expires_delta=timedelta(minutes=30),
        )
        refresh_token = utils.create_token(
            data={"user_id": user_id}, expires_delta=timedelta(days=7)
        )
        return {
            "token_type": "bearer",
            "access_token": access_token,
            "refresh_token": refresh_token,
        }

    async def refresh_access_token(self, refresh_token: str) -> dict:
        if await is_token_blacklisted(refresh_token):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is blacklisted"
            )

        payload = utils.validate_token(refresh_token)
        user_id = payload.get("user_id")

        user = await self.user_repository.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        await add_token_to_blacklist(refresh_token, expiry_time_in_seconds=60 * 30)

        new_access_token = utils.create_token(
            data={
                "user_id": user_id,
                "group_id": user.group_id,
                "username": user.username,
                "role": user.role.value,
            },
            expires_delta=timedelta(minutes=30),
        )
        new_refresh_token = utils.create_token(
            data={"user_id": user_id}, expires_delta=timedelta(days=7)
        )
        return {
            "token_type": "bearer",
            "access_token": new_access_token,
            "refresh_token": new_refresh_token,
        }

    async def forgot_password(self, email: str, base_url: str):
        user = await self.user_repository.get_user_by_email(email=email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        try:
            access_token = utils.create_token(
                data={"sub": str(user.email)}, expires_delta=timedelta(minutes=10)
            )
            reset_link = utils.create_reset_link(token=access_token, base_url=base_url)
            body = utils.create_message(
                user_id=str(user.id), email=email, reset_link=reset_link
            )

            await producer.message_sender(body=body)

            return {
                "result": f"An email has been sent to {email} with a link for password reset."
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to send email: {e}")

    async def reset_password(self, token: str, new_password: str):
        if await is_token_blacklisted(token):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is blacklisted"
            )

        try:
            payload = utils.validate_token(token)
            email = payload.get("sub")
            user = await self.user_repository.user_reset_password(
                email=email, password=new_password
            )
            if user:
                await add_token_to_blacklist(token, expiry_time_in_seconds=60 * 30)
                return {"result": "Password reset successfully"}

        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Failed to reset password: {e}"
            )
