from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from src.auth.schemas import RefreshTokenRequest, Token, UserModel
from src.auth.service import AuthService
from src.repositories.user_repository import UserRepository

router = APIRouter(tags=["auth"], prefix="/auth")


@router.post("/signup", response_model=UserModel)
async def create_user(
    request: UserModel, user_repository: UserRepository = Depends(UserRepository)
):
    auth_service = AuthService(user_repository)
    new_user = await auth_service.create_new_user(request=request)
    return new_user


@router.post("/login", response_model=Token)
async def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_repository: UserRepository = Depends(UserRepository),
):
    auth_service = AuthService(user_repository)
    token_data = await auth_service.authenticate_user(form_data=form_data)
    return token_data


@router.post("/refresh-token", response_model=Token)
async def refresh_token(
    request: RefreshTokenRequest,
    user_repository: UserRepository = Depends(UserRepository),
):
    auth_service = AuthService(user_repository)
    token_data = await auth_service.refresh_access_token(
        refresh_token=request.refresh_token
    )
    return token_data
