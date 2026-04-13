from pydantic import BaseModel,Field
from beanie import Document
from typing import Optional
from datetime import datetime


class Order(Document):
    user_email:str
    product_id:str
    quantity:int
    total_price:float
    status:str

    payment_intent_id: Optional[str] = None
    refund_id: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name="orders"