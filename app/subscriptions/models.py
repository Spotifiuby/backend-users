import datetime

from fastapi import HTTPException
from moneyed import Money, USD
from pydantic import BaseModel


# Subscriptions
class SubscriptionType:
    name: str
    price: Money

    def __init__(self, name: str, price: Money):
        self.name = name
        self.price = price


basic = SubscriptionType("Basic", Money(1, USD))
pro = SubscriptionType("Pro", Money(10, USD))
premium = SubscriptionType("Premium", Money(100, USD))


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
