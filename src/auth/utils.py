from datetime import datetime, timedelta, timezone

from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from src.config import settings

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

SECRET_KEY = settings.secret_key
ALGORITHM = settings.ALGORITHM


def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)


def create_token(data: dict, expires_delta: timedelta) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def validate_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("exp") < datetime.now(tz=timezone.utc).timestamp():
            raise HTTPException(status_code=401, detail="Token expired")
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


def create_reset_link(token: str, base_url) -> str:
    return f"{base_url}auth/reset-password/{token}"


def create_message(user_id: str, email: str, reset_link: str) -> dict:
    return {
        "user_id": user_id,
        "email_address": email,
        "body": reset_link,
        "published_at": datetime.now().isoformat(),
    }
