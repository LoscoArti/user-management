import uuid

from src.repositories import user_repository
from src.user.dependencies import can_access_user_data
from src.user.schemas import UserUpdateSchema
from user.models import User


async def service_update_user(
    user_id: uuid.UUID, update_data: UserUpdateSchema, db
) -> User:
    return await user_repository.update_user(user_id, update_data, db)


async def service_delete_user(user_id: uuid.UUID, db) -> User:
    return await user_repository.delete_user(user_id, db)


async def service_get_user_by_id(user_id: uuid.UUID, current_user: User, db) -> User:
    able_to_access = await can_access_user_data(
        target_user_id=user_id, current_user=current_user, db=db
    )
    if able_to_access:
        user = await user_repository.get_user_by_id(user_id, db)
        return user
