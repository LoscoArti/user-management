from fastapi import HTTPException, status

from auth.utils import create_access_token, create_refresh_token, validate_refresh_token
from src.repositories.user_repository import UserRepository
from user.models import User


class AuthService:
    def __init__(self, auth_repository: UserRepository):
        self.auth_repository = auth_repository

    async def create_new_user(self, request) -> User:
        if await self.auth_repository.verify_user_exist(email=request.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )
        new_user = await self.auth_repository.create_user(request)
        return new_user

    async def authenticate_user(self, form_data) -> dict:
        user = await self.auth_repository.get_user_by_credentials(
            form_data.username, form_data.password
        )
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
            )
        user_id = str(user.id)
        token = create_access_token(
            data={
                "sub": user_id,
                "username": user.username,
                "role": user.role.value,
            }
        )
        refresh_token = create_refresh_token(data={"sub": user_id})
        return {
            "access_token": token,
            "token_type": "bearer",
            "refresh_token": refresh_token,
        }

    async def refresh_access_token(self, refresh_token: str) -> dict:
        payload = validate_refresh_token(refresh_token)
        user_id = payload.get("sub")

        user = await self.auth_repository.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        new_access_token = create_access_token(
            data={"sub": user_id, "username": user.username, "role": user.role.value}
        )
        new_refresh_token = create_refresh_token(data={"sub": user_id})
        return {
            "access_token": new_access_token,
            "token_type": "bearer",
            "refresh_token": new_refresh_token,
        }
