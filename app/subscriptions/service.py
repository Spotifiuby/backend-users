from fastapi import HTTPException

from app.database import conn
from app.subscriptions.models import UserSubscriptionRequest, UserSubscriptionModel, _validate_subscription_type_id
from app.subscriptions.models import basic, pro, premium
from app.settings import Settings
import requests

settings = Settings()



def create(body: UserSubscriptionRequest):
    _validate_subscription_type_id(body.subscription_type_id)

    m = conn.subscriptions.find_one({"user_id": body.user_id})
    if m:
        raise HTTPException(status_code=400, detail="User already subscribed.")

    s = UserSubscriptionModel(body.user_id, body.subscription_type_id)
    conn.subscriptions.insert_one(s.to_dict())

    price = 0
    if basic.name == body.subscription_type_id:
        price = basic.price
    elif pro.name == body.subscription_type_id:
        price = pro.price
    elif premium.name == body.subscription_type_id:
        price = premium.price
    rBody = {
        "amountInEthers": str(price),
        "senderId": body.user_id,
        }
    r = requests.post(settings.PAYMENT_URL + "/deposit", json=rBody)
    if r.status_code == 400 and r.json()['code'] == 'INSUFFICIENT_FUNDS':
        raise HTTPException(status_code=400, detail="Insufficient Funds")
    return get(body.user_id)


def get(user_id: str):
    m = conn.subscriptions.find_one({"user_id": user_id})
    if not m:
        raise HTTPException(status_code=404, detail="Subscription not found for User.")
    return UserSubscriptionModel.from_mongo(m)


def delete(user_id: str):
    m = conn.subscriptions.find_one({"user_id": user_id})
    if not m:
        raise HTTPException(status_code=404, detail="Subscription not found for User.")
    m = conn.subscriptions.delete_one({"user_id": user_id})


def modify(body: UserSubscriptionRequest):
    _validate_subscription_type_id(body.subscription_type_id)

    delete(body.user_id)
    return create(body)


def save_token(user_id, token):
    m = conn.tokens.find_one({"user_id": user_id})
    if m:
        conn.tokens.delete_one({"user_id": user_id})

    conn.tokens.insert_one({"user_id": user_id, "token": token})


def get_token(user_id):
    m = conn.tokens.find_one({"user_id": user_id})
    if m:
        return {"user_id": m["user_id"], "token": m["token"]}
    else:
        return {}
