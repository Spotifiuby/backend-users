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
    db_user = models.User(username=user.username)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# from bson import ObjectId
# import pymongo
# import datetime
# from config.db import conn
# from models.user import TypeEnum

# def _user_entity(user) -> dict:
#     user["id"] = str(user.pop("_id"))
#     return user

# def get_all():
#     return [_user_entity(user) for user in conn.users.find()]

# def get(user_id: str):
#     user = conn.users.find_one({"_id": ObjectId(user_id)})
#     if user:
#         return _user_entity(user)
#     return None

# def create(user):
#     user_dict = user.dict()
#     user_dict["date_created"] = datetime.datetime.today()
#     r = conn.users.insert_one(user_dict)
#     mongo_user = conn.users.find_one({"_id": r.inserted_id})
#     return _user_entity(mongo_user)

# def update(user_id, user):
#     to_update = {k: v for k, v in user.dict().items() if v is not None}
#     updated_user = conn.users.find_one_and_update(
#         {"_id": ObjectId(user_id)},
#         {"$set": to_update},
#         return_document=pymongo.ReturnDocument.AFTER
#     )
#     return _user_entity(updated_user)

# def delete(user_id):
#     r = conn.users.delete_one({"_id": ObjectId(user_id)})
#     return r.delete_count > 0