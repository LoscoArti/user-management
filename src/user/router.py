import uuid
from typing import List, Optional

from fastapi import APIRouter, Depends, Query

from src.repositories.user_repository import UserRepository
from user.dependencies import get_current_user
from user.models import User
from user.schemas import UserDisplaySchema, UserUpdateSchema
from user.service import UserService

router = APIRouter(tags=["user"], prefix="/user")


@router.get("/me", response_model=UserDisplaySchema)
async def read_user_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.patch("/me", response_model=UserDisplaySchema)
async def update_user_me(
    update_data: UserUpdateSchema,
    current_user: User = Depends(get_current_user),
    user_repository: UserRepository = Depends(UserRepository),
):
    user_service = UserService(user_repository)
    updated_user = await user_service.service_update_user(
        current_user=current_user, update_data=update_data, user_id=None
    )
    return updated_user


@router.delete("/me")
async def delete_user_me(
    current_user: User = Depends(get_current_user),
    user_repository: UserRepository = Depends(UserRepository),
):
    user_service = UserService(user_repository)
    deleted_user = await user_service.service_delete_user(user_id=current_user.id)
    return deleted_user


@router.get("/users", response_model=List[UserDisplaySchema])
async def list_users(
    page: int = Query(1, ge=1),
    limit: int = Query(30, ge=1),
    filter_by_name: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    user_repository: UserRepository = Depends(UserRepository),
):
    user_service = UserService(user_repository)
    users = await user_service.service_list_users(
        current_user=current_user,
        page=page,
        page_size=limit,
        filter_by_name=filter_by_name,
    )
    return users


@router.get("/{user_id}", response_model=UserDisplaySchema)
async def read_user_by_id(
    user_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    user_repository: UserRepository = Depends(UserRepository),
):
    user_service = UserService(user_repository)
    user = await user_service.service_get_user_by_id(
        user_id=user_id, current_user=current_user, user_repository=user_repository
    )
    return user


@router.patch("/{user_id}", response_model=UserDisplaySchema)
async def update_user_by_id(
    user_id: uuid.UUID,
    update_data: UserUpdateSchema,
    current_user: User = Depends(get_current_user),
    user_repository: UserRepository = Depends(UserRepository),
):
    user_service = UserService(user_repository)
    user = await user_service.service_update_user(
        current_user=current_user, user_id=user_id, update_data=update_data
    )
    return user


@router.delete("/{user_id}")
async def delete_user_by_id(
    user_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    user_repository: UserRepository = Depends(UserRepository),
):
    user_service = UserService(user_repository)
    user = await user_service.service_delete_user(
        user_id=user_id, current_user=current_user
    )
    return user
