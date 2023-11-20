from fastapi import HTTPException, status

from auth.utils import create_access_token, create_refresh_token, validate_refresh_token
from src.repositories.user_repository import (
    create_user,
    get_user_by_credentials,
    get_user_by_id,
    verify_user_exist,
)
from user.models import User


async def create_new_user(request, db) -> User:
    if await verify_user_exist(email=request.email, db=db):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    new_user = await create_user(request, db)
    return new_user


async def authenticate_user(form_data, db) -> dict:
    user = await get_user_by_credentials(
        username=form_data.username, password=form_data.password, db=db
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


async def refresh_access_token(refresh_token: str, db) -> dict:
    payload = validate_refresh_token(refresh_token)
    user_id = payload.get("sub")

    user = await get_user_by_id(user_id, db)
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
