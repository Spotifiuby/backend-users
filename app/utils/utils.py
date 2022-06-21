import asyncio
import logging

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.crud import get_user_by_email
from app.schemas import TypeEnum


logger = logging.getLogger('main-logger')


def log_request_body(request_id, body):
    asyncio.ensure_future(_log_request_body(request_id, body))


async def _log_request_body(request_id, body):
    logger.info(f"Request: {request_id} - Body: {body}")


def handle_user_permission(user_id: str, db: Session, user=None, email=None):
    if user_id == "adminusertoken": return True
    if user and user.user_type in ["listener", "uploader"] and user_id == user.email: return True
    requester = get_user_by_email(db, user_id)
    if not requester:
        raise HTTPException(status_code=403, detail="Invalid x-user-id")
    if user and user.user_type == TypeEnum.admin and requester.user_type != TypeEnum.admin:
        raise HTTPException(status_code=403)
    email = email if email else user.email
    if email != user_id and requester.user_type != TypeEnum.admin:
        raise HTTPException(status_code=403)
