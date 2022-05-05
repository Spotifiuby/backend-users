"""coding=utf-8"""
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    """User Class contains standard information for a User."""
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    is_active = Column(Boolean, default=True)
    first_name = Column(String, default="")
    last_name = Column(String, default="")
    user_type = Column(String)
    

# class UserModel(BaseModel):
#     id: str
#     username: str
#     first_name: Optional[str]
#     last_name: Optional[str]
#     user_type: TypeEnum
#     date_created: datetime.datetime

# class CreateUserRequest(BaseModel):
#     username: str
#     user_type: TypeEnum

# class UpdateSongRequest(BaseModel):
#     first_name: Optional[str]
#     last_name: Optional[str]
