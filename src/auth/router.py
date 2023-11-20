from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from auth.schemas import RefreshTokenRequest, Token, UserModel

# Import the AuthService class
from auth.service import AuthService
from database import get_session
from src.repositories.user_repository import UserRepository

router = APIRouter(tags=["auth"], prefix="/auth")


def get_auth_service(db: Session = Depends(get_session)):
    # :TODO: move this away form routers
    user_repository = UserRepository(db)
    return AuthService(user_repository)


@router.post("/signup", response_model=UserModel)
async def create_user(
    request: UserModel, auth_service: AuthService = Depends(get_auth_service)
):
    new_user = await auth_service.create_new_user(request)
    return new_user


@router.post("/login", response_model=Token)
async def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(get_auth_service),
):
    token_data = await auth_service.authenticate_user(form_data)
    return token_data


@router.post("/refresh-token", response_model=Token)
async def refresh_token(
    request: RefreshTokenRequest, auth_service: AuthService = Depends(get_auth_service)
):
    token_data = await auth_service.refresh_access_token(request.refresh_token)
    return token_data


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(get_auth_service),
):
    token_data = await auth_service.authenticate_user(form_data)
    return token_data
