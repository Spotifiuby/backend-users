import fastapi

import os

from fastapi import Security, Depends
from fastapi.openapi.models import APIKey
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.subscriptions import service
from app.subscriptions.models import UserSubscriptionRequest, UserSubscriptionResponse
from typing import Optional

from app.utils.utils import log_request_body, handle_user_permission


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_api_key(api_key_header: str = Security(APIKeyHeader(name="X-API-Key", auto_error=True))):
    if api_key_header in [os.getenv('BACKOFFICE_API_KEY'), os.getenv('NATIVE_APP_API_KEY')]:
        return api_key_header
    else:
        raise fastapi.HTTPException(status_code=403)


subscriptions_routes = fastapi.APIRouter()


@subscriptions_routes.post("/subscriptions", response_model=UserSubscriptionResponse, tags=["Subscriptions"],
                           status_code=fastapi.status.HTTP_201_CREATED)
async def create_subscription(body: UserSubscriptionRequest,
                              x_user_id: Optional[str] = fastapi.Header(None),
                              x_request_id: Optional[str] = fastapi.Header(None),
                              _: APIKey = Depends(get_api_key),
                              db: Session = Depends(get_db)):
    log_request_body(x_request_id, body)
    handle_user_permission(x_user_id, db, email=body.user_id)
    return service.create(body)


@subscriptions_routes.get("/subscriptions/{user_id}", response_model=UserSubscriptionResponse, tags=["Subscriptions"],
                          status_code=fastapi.status.HTTP_200_OK)
async def create_subscription(user_id: str,
                              x_user_id: Optional[str] = fastapi.Header(None),
                              x_request_id: Optional[str] = fastapi.Header(None),
                              _: APIKey = Depends(get_api_key),
                              db: Session = Depends(get_db)):
    handle_user_permission(x_user_id, db, email=user_id)
    return service.get(user_id)
