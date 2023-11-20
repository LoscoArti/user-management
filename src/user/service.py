import uuid

from fastapi import HTTPException, status

from src.repositories.user_repository import UserRepository
from user.models import User


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.auth_repository = user_repository

    async def get_user_by_id(self, user_id: uuid.UUID) -> User:
        user = await self.user_repository.get_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        return user
