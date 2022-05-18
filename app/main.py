"""coding=utf-8."""
from typing import List
import uvicorn
from fastapi import Depends, FastAPI, HTTPException, status, Security
from fastapi.security.api_key import APIKeyHeader, APIKey
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine
from .settings import Settings

models.Base.metadata.create_all(bind=engine)

settings = Settings()

app = FastAPI()


#Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

API_KEY = settings.API_KEY
API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)

async def get_api_key(
    api_key_header: str = Security(api_key_header),
):
    if api_key_header == API_KEY:
        return api_key_header
    else:
        raise HTTPException(status_code=403)

@app.post("/users/", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db), api_key: APIKey = Depends(get_api_key)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email %s already registered" % user.email)
    return crud.create_user(db=db, user=user)

@app.get("/users/", response_model=List[schemas.User], status_code=status.HTTP_200_OK)
def read_users( skip: int = 0,
                limit: int = 100,
                email: str = "",
                first_name: str = "",
                last_name: str = "",
                user_type: str = "",
                is_active: bool = True,
                db: Session = Depends(get_db),
                api_key: APIKey = Depends(get_api_key)
                ):
    users = crud.get_users(db, skip, limit, email, first_name, last_name, user_type, is_active)
    return users

@app.get("/users/{email}", response_model=schemas.User, status_code=status.HTTP_200_OK)
def read_user(email: str, db: Session = Depends(get_db), api_key: APIKey = Depends(get_api_key)):
    db_user = crud.get_user(db, email=email)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return db_user

@app.delete("/users/{email}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(email: str, db: Session = Depends(get_db), api_key: APIKey = Depends(get_api_key)):
    # _check_vlaid_user_id(user_id)
    r = crud.delete_user(db, email=email)  

@app.put("/users/{email}", response_model=schemas.User)
def update_user(email:str, user: schemas.UserUpdate, db: Session = Depends(get_db), api_key: APIKey = Depends(get_api_key)):
    updated_user = crud.updated_user(db=db, email=email, user=user)
    if not updated_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return updated_user

# To run locally
if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)