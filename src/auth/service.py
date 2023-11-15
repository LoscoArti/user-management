from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from auth.utils import create_access_token, get_hashed_password, verify_password
from user.models import User


async def create_new_user(request, database) -> User:
    if await verify_user_exist(database, email=request.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    hashed_password = get_hashed_password(request.password)
    new_user = User(
        name=request.name,
        email=request.email,
        hashed_password=hashed_password,
        username=request.username,
        phone_number=request.phone_number,
        surname=request.surname,
    )

    database.add(new_user)
    await database.commit()
    return new_user


async def authenticate_user(request, database) -> dict:
    check_user = await verify_user_exist(database, username=request.username)
    if not check_user or not verify_password(
        request.password, check_user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    user_id = str(check_user.id)
    token = create_access_token(
        data={
            "sub": user_id,
            "username": check_user.username,
            "role": check_user.role.value,
        }
    )
    return {"access_token": token, "token_type": "bearer"}


async def verify_user_exist(db_session: Session, **kwargs) -> Optional[User]:
    query = select(User)
    for attr, value in kwargs.items():
        query = query.filter(getattr(User, attr) == value)
    result = await db_session.execute(query)
    return result.scalars().first()
