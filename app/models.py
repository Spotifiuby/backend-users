"""coding=utf-8"""
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from .database import Base
from .schemas import TypeEnum

class User(Base):
    """User Class contains standard information for a User."""
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    is_active = Column(Boolean, default=True)
    first_name = Column(String, default="")
    last_name = Column(String, default="")
    user_type = Column(String)
