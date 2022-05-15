"""coding=utf-8."""
from typing import List
import uvicorn
from fastapi import Depends, FastAPI, HTTPException, status
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

@app.post("/users/", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email %s already registered" % user.email)
    return crud.create_user(db=db, user=user)

@app.get("/users/", response_model=List[schemas.User], status_code=status.HTTP_200_OK)
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.get("/users/{email}", response_model=schemas.User, status_code=status.HTTP_200_OK)
def read_user(email: str, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, email=email)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return db_user

@app.delete("/users/{email}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(email: str, db: Session = Depends(get_db)):
    # _check_vlaid_user_id(user_id)
    r = crud.delete_user(db, email=email)  

@app.put("/users/{email}", response_model=schemas.User)
def update_user(email:str, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    updated_user = crud.updated_user(db=db, email=email, user=user)
    if not updated_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return updated_user

# To run locally
if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)