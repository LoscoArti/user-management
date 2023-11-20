from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_session
from src.repositories.user_repository import UserRepository
from user.dependencies import get_current_user
from user.models import User
from user.schemas import UserDisplaySchema, UserUpdateSchema
from user.service import UserService

router = APIRouter(tags=["user"], prefix="/user")


def get_user_service(db: Session = Depends(get_session)):
    # :TODO: move this away form routers
    user_repository = UserRepository(db)
    return UserService(user_repository)


@router.get("/me", response_model=UserDisplaySchema)
async def read_user_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.patch("/me", response_model=UserDisplaySchema)
async def update_user_me(
    update_data: UserUpdateSchema,
    current_user: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service),
):
    updated_user = await user_service.update_user(current_user.id, update_data)
    return updated_user


@router.delete("/me")
async def delete_user_me(
    current_user: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service),
):
    deleted_user = await user_service.delete_user(current_user.id)
    return deleted_user
