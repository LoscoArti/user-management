import uuid
from typing import Optional

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from auth.utils import get_hashed_password, verify_password
from src.user.schemas import UserUpdateSchema
from user.models import User


async def create_user(user_data, db: Session) -> User:
    hashed_password = get_hashed_password(user_data.hashed_password)
    new_user = User(
        name=user_data.name,
        email=user_data.email,
        hashed_password=hashed_password,
        username=user_data.username,
        phone_number=user_data.phone_number,
        surname=user_data.surname,
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


async def get_user_by_credentials(
    username: str, password: str, db: Session
) -> Optional[User]:
    user = await get_user_by_username(username, db)
    if user and verify_password(password, user.hashed_password):
        return user
    return None


async def get_user_by_username(username: str, db: Session) -> Optional[User]:
    query = select(User).filter_by(username=username)
    result = await db.execute(query)
    return result.scalars().first()


async def get_user_by_id(user_id: uuid.UUID, db: Session) -> Optional[User]:
    query = select(User).filter_by(id=user_id)
    result = await db.execute(query)
    return result.scalars().first()


async def verify_user_exist(db: Session, **kwargs) -> bool:
    query = select(User)
    for attr, value in kwargs.items():
        query = query.filter(getattr(User, attr) == value)
    result = await db.execute(query)
    return result.scalars().first() is not None


async def update_user(
    user_id: uuid.UUID, update_data: UserUpdateSchema, db: Session
) -> User:
    user = await get_user_by_id(user_id, db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    update_data_dict = update_data.dict(exclude_unset=True)

    allowed_update_fields = ["username", "email", "name", "surname", "phone_number"]

    for key in allowed_update_fields:
        if key in update_data_dict:
            setattr(user, key, update_data_dict[key])

    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def delete_user(user_id: uuid.UUID, db: Session) -> None:
    user = await get_user_by_id(user_id, db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await db.delete(user)
    await db.commit()
