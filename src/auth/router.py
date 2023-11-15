from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from auth import service as auth_service
from auth.schemas import Token, UserModel
from database import get_session

router = APIRouter(tags=["auth"], prefix="/auth")


@router.post("/signup", response_model=UserModel)
async def create_user(request: UserModel, database: Session = Depends(get_session)):
    new_user = await auth_service.create_new_user(request=request, database=database)
    return new_user


@router.post("/login", response_model=Token)
async def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    database: Session = Depends(get_session),
):
    token_data = await auth_service.authenticate_user(
        form_data=form_data, database=database
    )
    return token_data
