import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_session
from user.dependencies import get_current_user
from user.models import User
from user.schemas import UserDisplaySchema, UserUpdateSchema
from user.service import (
    service_delete_user,
    service_get_user_by_id,
    service_update_user,
)

router = APIRouter(tags=["user"], prefix="/user")


@router.get("/me", response_model=UserDisplaySchema)
async def read_user_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.patch("/me", response_model=UserDisplaySchema)
async def update_user_me(
    update_data: UserUpdateSchema,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session),
):
    updated_user = await service_update_user(current_user.id, update_data, db)
    return updated_user


@router.delete("/me")
async def delete_user_me(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_session)
):
    deleted_user = await service_delete_user(current_user.id, db)
    return deleted_user


@router.get("/{user_id}", response_model=UserDisplaySchema)
async def read_user_by_id(
    user_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session),
):
    user = await service_get_user_by_id(user_id, current_user, db)
    return user
