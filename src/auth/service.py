from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from user.models import User

from .utils import get_hashed_password


async def create_new_user(request, database) -> User:
    if await verify_email_exist(email=request.email, db_session=database):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    hashed_password = get_hashed_password(request.password)
    new_user = User(
        name=request.name,
        email=request.email,
        password=hashed_password,
        username=request.username,
        phone_number=request.phone_number,
        surname=request.surname,
    )

    database.add(new_user)
    await database.commit()
    await database.close()
    return new_user


async def verify_email_exist(email: str, db_session: Session) -> Optional[User]:
    query = select(User).filter(User.email == email)
    result = await db_session.execute(query)
    user = result.scalars().first()
    return user
