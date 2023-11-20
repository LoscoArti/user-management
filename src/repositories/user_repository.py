from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from auth.utils import get_hashed_password, verify_password
from user.models import User


class UserRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

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
        self.db_session.add(new_user)
        await self.db_session.commit()
        await self.db_session.refresh(new_user)
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
        result = await self.db_session.execute(query)
        return result.scalars().first()

    async def get_user_by_id(self, user_id: str) -> Optional[User]:
        query = select(User).filter_by(id=user_id)
        result = await self.db_session.execute(query)
        return result.scalars().first()

    async def verify_user_exist(self, **kwargs) -> bool:
        query = select(User)
        for attr, value in kwargs.items():
            query = query.filter(getattr(User, attr) == value)
        result = await self.db_session.execute(query)
        return result.scalars().first() is not None
