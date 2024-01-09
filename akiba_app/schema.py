# Pydantic models

from pydantic import BaseModel
from datetime import datetime

class UserBase(BaseModel):
    firstname: str
    lastname: str
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: str
    registered_on: datetime


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None
