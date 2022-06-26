"""coding=utf-8."""
from sqlalchemy.orm import Session
from . import models, schemas
from .settings import Settings
import requests

settings = Settings()


def get_user(db: Session, email: str):
    user = db.query(models.User).filter(models.User.email == email).first()
    if user:
        r = requests.get(settings.PAYMENT_URL + "/wallet/%s" % email)
        user.wallet_address = r.json()['address'] if r.status_code == 200 else 'No wallet found. Please contact administrator.'
    return user

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users( db,
               skip: int = 0,
               limit: int = 100,
               email: str = "",
               first_name: str = "",
               last_name: str = "",
               user_type: str = "",
               is_active: bool = None
               ):
    
    q = db.query(models.User).filter(
        models.User.email.ilike("%{}%".format(email)),
        models.User.first_name.ilike("%{}%".format(first_name)),
        models.User.last_name.ilike("%{}%".format(last_name)),
        models.User.user_type.ilike("%{}%".format(user_type))
        ) 
    if is_active is not None:
        q = q.filter(models.User.is_active == is_active)
    return q.offset(skip).limit(limit).all()

def create_user(db:Session, user: schemas.UserCreate):
    db_user = models.User(email=user.email, first_name=user.first_name, last_name=user.last_name, user_type=user.user_type)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    body = {
        'userId': user.email
    }
    x = requests.post(settings.PAYMENT_URL + '/wallet', json = body)
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
        models.User.is_active: user.is_active if user.is_active is not None else db_user.is_active,
    }
    db.query(models.User).filter(models.User.email == email).update(values)
    db.commit()
    db.refresh(db_user)
    return db_user