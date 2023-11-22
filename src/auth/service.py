from datetime import timedelta

from fastapi import HTTPException, status

from auth import utils
from src.repositories import user_repository
from user.models import User


async def create_new_user(request, db) -> User:
    if await user_repository.verify_user_exist(email=request.email, db=db):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    new_user = await user_repository.create_user(request, db)
    return new_user


async def authenticate_user(form_data, db) -> dict:
    user = await user_repository.get_user_by_credentials(
        username=form_data.username, password=form_data.password, db=db
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    user_id = str(user.id)
    access_token = utils.create_token(
        data={
            "sub": user_id,
            "username": user.username,
            "role": user.role.value,
        },
        expires_delta=timedelta(minutes=30),
    )
    refresh_token = utils.create_token(
        data={"sub": user_id}, expires_delta=timedelta(days=7)
    )
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


async def refresh_access_token(refresh_token: str, db) -> dict:
    payload = utils.validate_token(refresh_token)
    user_id = payload.get("sub")

    user = await user_repository.get_user_by_id(user_id, db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    new_access_token = utils.create_token(
        data={
            "sub": user_id,
            "username": user.username,
            "role": user.role.value,
        },
        expires_delta=timedelta(minutes=30),
    )
    new_refresh_token = utils.create_token(
        data={"sub": user_id}, expires_delta=timedelta(days=7)
    )
    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer",
    }
