import datetime
import uuid
from typing import Optional

from pydantic import BaseModel, EmailStr, validator


class UserBaseSchema(BaseModel):
    username: str
    email: EmailStr
    hashed_password: str
    name: str
    surname: str
    phone_number: str


class UserUpdateSchema(BaseModel):
    username: Optional[str]
    email: Optional[EmailStr]
    name: Optional[str]
    surname: Optional[str]
    phone_number: Optional[str]


class UserDisplaySchema(BaseModel):
    id: str
    username: str
    email: EmailStr
    name: str
    surname: str
    phone_number: str
    role: str
    created_at: str
    updated_at: Optional[str] = None

    @validator("id", "created_at", "updated_at", pre=True, allow_reuse=True)
    def convert_to_string(cls, value):
        if isinstance(value, uuid.UUID):
            return str(value)
        elif isinstance(value, datetime.datetime):
            return value.isoformat()
