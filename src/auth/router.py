from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from auth import service
from auth.schemas import RefreshTokenRequest, Token, UserModel
from database import get_session

router = APIRouter(tags=["auth"], prefix="/auth")


@router.post("/signup", response_model=UserModel)
async def create_user(request: UserModel, db: Session = Depends(get_session)):
    new_user = await service.create_new_user(request, db)
    return new_user


@router.post("/login", response_model=Token)
async def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_session)
):
    token_data = await service.authenticate_user(form_data, db)
    return token_data


@router.post("/refresh-token", response_model=Token)
async def refresh_token(
    request: RefreshTokenRequest, db: Session = Depends(get_session)
):
    token_data = await service.refresh_access_token(request.refresh_token, db)
    return token_data
