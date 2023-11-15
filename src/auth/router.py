from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from auth.schemas import UserModel
from database import get_session

from . import service as auth_service

router = APIRouter(tags=["auth"], prefix="/auth")


@router.post("/signup")
async def create_user(request: UserModel, database: Session = Depends(get_session)):
    new_user = await auth_service.create_new_user(request=request, database=database)
    return new_user
