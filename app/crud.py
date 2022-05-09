"""coding=utf-8."""
from sqlalchemy.orm import Session
from . import models, schemas

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_users(db:Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db:Session, user: schemas.UserCreate):
    db_user = models.User(username=user.username, first_name=user.first_name, last_name=user.last_name, user_type=user.user_type)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db:Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        return False
    db.delete(db_user)
    db.commit()
    return True

def updated_user(db: Session, user_id: int, user: schemas.UserUpdate):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        return False
    values = {
        models.User.first_name: user.first_name if user.first_name else db_user.first_name,
        models.User.last_name: user.last_name if user.last_name else db_user.last_name,
        models.User.user_type: user.user_type if user.user_type else db_user.user_type,
    }
    db.query(models.User).filter(models.User.id == user_id).update(values)
    db.commit()
    db.refresh(db_user)
    return db_user


