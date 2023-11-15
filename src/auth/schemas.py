from pydantic import BaseModel, EmailStr


class UserModel(BaseModel):
    username: str
    email: EmailStr
    hashed_password: str
    name: str
    surname: str
    phone_number: str


class Token(BaseModel):
    access_token: str
    token_type: str
