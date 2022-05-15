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
    email: str

class UserCreate(UserBase):
    first_name: Optional[str]
    last_name: Optional[str]
    user_type: TypeEnum
    date_created: datetime.datetime

class UserUpdate(UserBase):
    first_name: Optional[str]
    last_name: Optional[str]
    user_type: Optional[TypeEnum]

class User(UserBase):
    id: int
    first_name: str
    last_name: str
    user_type: TypeEnum
    is_active: bool

    class Config:
        orm_mode = True