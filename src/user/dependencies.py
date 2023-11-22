import uuid

from fastapi import Depends, HTTPException, status
from jose import JWTError
from sqlalchemy.orm import Session

from auth.utils import oauth2_scheme, validate_token
from database import get_session
from src.repositories.user_repository import get_user_by_id
from user.models import Role, User


async def get_current_user(
    db: Session = Depends(get_session), token: str = Depends(oauth2_scheme)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = validate_token(token)
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await get_user_by_id(user_id, db)
    if user is None:
        raise credentials_exception
    return user


async def can_access_user_data(
    target_user_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session),
) -> bool:
    if current_user.role == Role.ADMIN:
        return True

    elif current_user.role == Role.MODERATOR:
        target_user = await get_user_by_id(user_id=target_user_id, db=db)
        if target_user and target_user.group_id == current_user.group_id:
            return True
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this user's data.",
            )

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="You do not have permission to access this user's data.",
    )
