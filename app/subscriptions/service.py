from fastapi import HTTPException

from app.database import conn
from app.subscriptions.models import UserSubscriptionRequest, UserSubscriptionModel, _validate_subscription_type_id


def create(body: UserSubscriptionRequest):
    _validate_subscription_type_id(body.subscription_type_id)
    # TODO: Validar que el usuario exista
    # TODO: Validar que no haya una suscripción ya creada para el usuario
    s = UserSubscriptionModel(body.user_id, body.subscription_type_id)
    conn.subscriptions.insert_one(s.to_dict())

    # TODO: Procesar pago
    return get(body.user_id)


def get(user_id: str):
    m = conn.subscriptions.find_one({"user_id": user_id})
    if not m:
        raise HTTPException(status_code=404, detail="Subscription not found for User")
    return UserSubscriptionModel.from_mongo(m)
