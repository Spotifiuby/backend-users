import datetime

from fastapi import HTTPException
from decimal import Decimal
from pydantic import BaseModel


# Subscriptions
class SubscriptionType:
    name: str
    price: Decimal

    def __init__(self, name: str, price: Decimal):
        self.name = name
        self.price = price


basic = SubscriptionType("Basic", Decimal("0.000001"))
pro = SubscriptionType("Pro", Decimal("0.000002"))
premium = SubscriptionType("Premium", Decimal("0.000003"))


def _validate_subscription_type_id(t: str):
    if t in [basic.name, pro.name, premium.name]:
        return
    else:
        raise HTTPException(status_code=400, detail="Invalid Subscription Type")


# User-Subscription
class UserSubscriptionModel:
    id: str
    user_id: str
    subscription_type_id: str
    date_subscribed: datetime.datetime
    last_payed: datetime.datetime

    def __init__(self, user_id: str, subscription_type_id: str):
        self.user_id = user_id
        self.subscription_type_id = subscription_type_id
        self.date_subscribed = datetime.datetime.today()
        self.last_payed = datetime.datetime.today()

    def to_dict(self):
        r = {
            "user_id": self.user_id,
            "subscription_type_id": self.subscription_type_id,
            "date_subscribed": self.date_subscribed,
            "last_payed": self.last_payed,
        }

        if hasattr(self, "id"):
            r["id"] = self.id

        return r

    @classmethod
    def from_mongo(cls, m):
        m["id"] = str(m.pop("_id"))
        return m


class UserSubscriptionRequest(BaseModel):
    user_id: str
    subscription_type_id: str


class UserSubscriptionResponse(BaseModel):
    id: str
    user_id: str
    subscription_type_id: str
    date_subscribed: datetime.datetime
    last_payed: datetime.datetime
