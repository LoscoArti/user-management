import uuid
from typing import List, Optional

from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from auth.utils import get_hashed_password, verify_password
from src.database import get_session
from src.user.schemas import UserUpdateSchema
from user.models import User


class UserRepository:
    def __init__(self, db: Session = Depends(get_session)):
        self.db = db

    async def create_user(self, user_data) -> User:
        hashed_password = get_hashed_password(user_data.hashed_password)
        new_user = User(
            name=user_data.name,
            email=user_data.email,
            hashed_password=hashed_password,
            username=user_data.username,
            phone_number=user_data.phone_number,
            surname=user_data.surname,
        )
        self.db.add(new_user)
        await self.db.commit()
        await self.db.refresh(new_user)
        return new_user

    async def get_user_by_credentials(
        self, username: str, password: str
    ) -> Optional[User]:
        user = await self.get_user_by_username(username)
        if user and verify_password(password, user.hashed_password):
            return user
        return None

    async def get_user_by_username(self, username: str) -> Optional[User]:
        query = select(User).filter_by(username=username)
        result = await self.db.execute(query)
        return result.scalars().first()

    async def get_user_by_id(self, user_id: uuid.UUID) -> Optional[User]:
        query = select(User).filter_by(id=user_id)
        result = await self.db.execute(query)
        return result.scalars().first()

    async def verify_user_exist(self, **kwargs) -> bool:
        query = select(User)
        for attr, value in kwargs.items():
            query = query.filter(getattr(User, attr) == value)
        result = await self.db.execute(query)
        return result.scalars().first() is not None

    async def update_user(
        self, user_id: uuid.UUID, update_data: UserUpdateSchema
    ) -> User:
        user = await self.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        update_data_dict = update_data.model_dump(exclude_unset=True)

        allowed_update_fields = ["username", "email", "name", "surname", "phone_number"]

        for key in allowed_update_fields:
            if key in update_data_dict:
                setattr(user, key, update_data_dict[key])

        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def delete_user(self, user_id: uuid.UUID) -> None:
        user = await self.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        await self.db.delete(user)
        await self.db.commit()

    async def list_users(
        self,
        page: int,
        page_size: int,
        filter_by_name: Optional[str] = None,
        group_id: Optional[int] = None,
    ) -> List[User]:
        query = select(User).limit(page_size).offset((page - 1) * page_size)

        if group_id is not None:
            query = query.filter(User.group_id == group_id)

        if filter_by_name:
            name_filter = f"%{filter_by_name}%"
            query = query.filter(User.name.ilike(name_filter))

        result = await self.db.execute(query)
        return result.scalars().all()
