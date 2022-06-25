"""coding=utf-8."""
from typing import Optional
from pydantic import BaseModel
from enum import Enum

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

class UserUpdate(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    user_type: Optional[TypeEnum]
    is_active: Optional[bool]

class User(UserBase):
    id: int
    first_name: str
    last_name: str
    user_type: TypeEnum
    is_active: bool
    wallet_address: Optional[str]

    class Config:
        orm_mode = True