"""coding=utf-8."""
from sqlalchemy.orm import Session
from . import models, schemas

def get_user(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db:Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db:Session, user: schemas.UserCreate):
    db_user = models.User(email=user.email, first_name=user.first_name, last_name=user.last_name, user_type=user.user_type)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db:Session, email: str):
    db_user = db.query(models.User).filter(models.User.email == email).first()
    if not db_user:
        return False
    db.delete(db_user)
    db.commit()
    return True

def updated_user(db: Session, email: str, user: schemas.UserUpdate):
    db_user = db.query(models.User).filter(models.User.email == email).first()
    if not db_user:
        return False
    values = {
        models.User.first_name: user.first_name if user.first_name else db_user.first_name,
        models.User.last_name: user.last_name if user.last_name else db_user.last_name,
        models.User.user_type: user.user_type if user.user_type else db_user.user_type,
    }
    db.query(models.User).filter(models.User.email == email).update(values)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users_ilike(db,
                    skip: int = 0,
                    limit: int = 100,
                    email: str = "",
                    first_name: str = "",
                    last_name: str = "",
                    user_type: str = "",
                    is_active: bool = True
                    ):
    return db.query(models.User).filter(
        models.User.email.ilike("%{}%".format(email)),
        models.User.first_name.ilike("%{}%".format(first_name)),
        models.User.last_name.ilike("%{}%".format(last_name)),
        models.User.user_type.ilike("%{}%".format(user_type)),
        models.User.is_active == is_active
        ).offset(skip).limit(limit).all()