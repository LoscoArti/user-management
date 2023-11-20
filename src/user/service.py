import uuid

from src.repositories.user_repository import UserRepository
from src.user.schemas import UserUpdateSchema
from user.models import User


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def update_user(
        self, user_id: uuid.UUID, update_data: UserUpdateSchema
    ) -> User:
        return await self.user_repository.update_user(user_id, update_data)

    async def delete_user(self, user_id: uuid.UUID) -> User:
        return await self.user_repository.delete_user(user_id)
