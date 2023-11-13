from pydantic import BaseModel


class UserModel(BaseModel):
    username: str
    email: str
    password: str
    name: str
    surname: str
    phone_number: str
