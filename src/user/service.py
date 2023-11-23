import uuid
from typing import List, Optional

from fastapi import HTTPException

from src.repositories.user_repository import UserRepository
from src.user.dependencies import can_access_user_data
from src.user.schemas import UserUpdateSchema
from user.models import Role, User


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def service_update_user(
        self, current_user: User, update_data: UserUpdateSchema, user_id: uuid.UUID
    ) -> User:
        target_user_id = user_id if user_id is not None else current_user.id
        is_admin = current_user.role == Role.ADMIN

        if is_admin or current_user.id == target_user_id:
            return await self.user_repository.update_user(
                user_id=target_user_id, update_data=update_data
            )
        else:
            raise HTTPException(
                status_code=403, detail="Insufficient permissions to update this user"
            )

    async def service_delete_user(self, user_id: uuid.UUID, current_user: User) -> User:
        target_user_id = user_id if user_id is not None else current_user.id
        is_admin = current_user.role == Role.ADMIN

        if is_admin or current_user.id == target_user_id:
            return await self.user_repository.delete_user(target_user_id)
        else:
            raise HTTPException(
                status_code=403, detail="Insufficient permissions to delete this user"
            )

    async def service_get_user_by_id(
        self, user_id: uuid.UUID, current_user: User, user_repository: UserRepository
    ) -> User:
        able_to_access = await can_access_user_data(
            target_user_id=user_id, current_user=current_user, db=user_repository.db
        )
        if able_to_access:
            user = await self.user_repository.get_user_by_id(user_id=user_id)
            return user

    async def service_list_users(
        self,
        current_user: User,
        page: int = 1,
        page_size: int = 10,
        filter_by_name: Optional[str] = None,
    ) -> List[User]:
        if current_user.role == Role.ADMIN:
            return await self.user_repository.list_users(
                page=page,
                page_size=page_size,
                filter_by_name=filter_by_name,
            )
        elif current_user.role == Role.MODERATOR:
            # Moderators can only list users from their own group
            return await self.user_repository.list_users(
                page=page,
                page_size=page_size,
                filter_by_name=filter_by_name,
                group_id=current_user.group_id,
            )
        else:
            raise HTTPException(
                status_code=403, detail="Insufficient permissions to list users"
            )
