"""coding=utf-8."""
from typing import List
import uvicorn
from fastapi import Depends, FastAPI, HTTPException, status, Security, Header
from fastapi.security.api_key import APIKeyHeader, APIKey
from sqlalchemy.orm import Session
from typing import Optional

from app.subscriptions.controller import subscriptions_routes
from . import crud, models, schemas
from .database import SessionLocal, engine
from .settings import Settings
from logging.config import dictConfig
from .config.log_conf import log_config
from .utils.utils import log_request_body, handle_user_permission

models.Base.metadata.create_all(bind=engine)

settings = Settings()

dictConfig(log_config)

app = FastAPI()


#Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

BACKOFFICE_API_KEY = settings.BACKOFFICE_API_KEY
NATIVE_APP_API_KEY = settings.NATIVE_APP_API_KEY
API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)

async def get_api_key(
    api_key_header: str = Security(api_key_header),
):
    if api_key_header in [BACKOFFICE_API_KEY, NATIVE_APP_API_KEY]:
        return api_key_header
    else:
        raise HTTPException(status_code=403)

@app.post("/users/", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db), api_key: APIKey = Depends(get_api_key), x_request_id: Optional[str] = Header(None), x_user_id: Optional[str] = Header(None)):
    log_request_body(x_request_id, {"user": user})
    handle_user_permission(x_user_id, db=db, user=user)
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email %s already registered" % user.email)
    return crud.create_user(db=db, user=user)

@app.get("/users/", response_model=List[schemas.User], status_code=status.HTTP_200_OK)
async def read_users( skip: int = 0,
                limit: int = 100,
                email: str = "",
                first_name: str = "",
                last_name: str = "",
                user_type: str = "",
                is_active: bool = None,
                db: Session = Depends(get_db),
                api_key: APIKey = Depends(get_api_key)
                ):
    users = crud.get_users(db, skip, limit, email, first_name, last_name, user_type, is_active)
    return users

@app.get("/users/{email}", response_model=schemas.User, status_code=status.HTTP_200_OK)
async def read_user(email: str, db: Session = Depends(get_db), api_key: APIKey = Depends(get_api_key)):
    db_user = crud.get_user(db, email=email)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return db_user

@app.delete("/users/{email}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(email: str, db: Session = Depends(get_db), api_key: APIKey = Depends(get_api_key), x_request_id: Optional[str] = Header(None), x_user_id: Optional[str] = Header(None)):
    handle_user_permission(x_user_id, db=db, email=email)
    r = crud.delete_user(db, email=email)  

@app.put("/users/{email}", response_model=schemas.User)
async def update_user(email:str, user: schemas.UserUpdate, db: Session = Depends(get_db), api_key: APIKey = Depends(get_api_key), x_request_id: Optional[str] = Header(None), x_user_id: Optional[str] = Header(None)):
    log_request_body(x_request_id, {"user-email": email, "user-update": user})
    handle_user_permission(x_user_id, db=db, user=user, email=email)
    updated_user = crud.updated_user(db=db, email=email, user=user)
    if not updated_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return updated_user

app.include_router(subscriptions_routes)

# To run locally
if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)