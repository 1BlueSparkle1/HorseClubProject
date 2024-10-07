from datetime import date

from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import mapped_column


class UserBase(BaseModel):
    surname: str
    name: str
    birthday: date
    login: str = mapped_column(unique=True)
    password: bytes
    role: str


class UserCreate(UserBase):
    password: str


class UserUpdate(UserCreate):
    pass


class UserUpdatePartial(UserCreate):
    surname: str | None = None
    name: str | None = None
    birthday: date | None = None
    login: str | None = None
    password: str | None = None
    role: str | None = None


class User(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
