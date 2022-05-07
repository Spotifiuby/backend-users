"""coding=utf-8."""
from typing import Optional
from pydantic import BaseModel
from enum import Enum
import datetime

class TypeEnum(str, Enum):
    uploader = "uploader"
    admin = "admin"
    listener = "listener"

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    first_name: Optional[str]
    last_name: Optional[str]
    user_type: TypeEnum
    date_created: datetime.datetime

class UserUpdate(UserBase):
    first_name: Optional[str]
    last_name: Optional[str]

class User(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True