"""coding=utf-8."""
from typing import List
import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

#Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username {user.username} already registered")
    return crud.create_user(db=db, user=user)

@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# To run locally
if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)

# import uvicorn
# from fastapi import FastAPI, Response
# from fastapi.middleware.cors import CORSMiddleware
# from docs import tags_metadata
# from routes.user import user_routes

# app = FastAPI(
#     title="Users backend for Spotifiuby",
#     description="REST API using FastAPI and PostgreSQL",
#     version="0.0.1",
#     openapi_tags=tags_metadata,
#     swagger_ui_parameters={"defaultModelsExpandDepth": -1}
# )

# # TODO: En producción no se podría dejar así
# origins = ["*"]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# app.include_router(user_routes)

# @app.get("/", include_in_schema=False)
# def ping():
#     return Response(status_code=200)

# if __name__ == "__main__":
#     uvicorn.run("main:app", host='0.0.0.0', port=8000, reload=True)