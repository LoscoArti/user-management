from fastapi import APIRouter, Depends

from user.dependencies import get_current_user
from user.models import User
from user.schemas import UserDisplaySchema

router = APIRouter(tags=["user"], prefix="/user")


@router.get("/me", response_model=UserDisplaySchema)
async def read_user_me(current_user: User = Depends(get_current_user)):
    return current_user
