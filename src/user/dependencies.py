from fastapi import Depends, HTTPException, status
from jose import JWTError
from sqlalchemy.orm import Session

from auth.utils import oauth2_scheme, validate_access_token
from database import get_session
from src.repositories.user_repository import UserRepository
from user.models import User


async def get_current_user(
    db: Session = Depends(get_session), token: str = Depends(oauth2_scheme)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = validate_access_token(token)
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user_repository = UserRepository(db)
    user = await user_repository.get_user_by_id(user_id)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_admin(
    current_user: User = Depends(get_current_user),
) -> User:  # find out better way to implement this including other roles and extracting role from jwt token
    if current_user.role not in [User.Role.ADMIN, User.Role.MODERATOR]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges",
        )
    return current_user
