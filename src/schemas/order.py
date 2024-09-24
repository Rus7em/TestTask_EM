from pydantic import BaseModel
from typing import List
from datetime import datetime

from order_item import CreateOrderItem, ReadOrderItem


class CreateOrder(BaseModel):
    state: str
    items: List[CreateOrderItem]


class ReadOrder(BaseModel):
    id: int
    create_at: datetime
    status_id: int
    items: List[ReadOrderItem]

    class Config:
        orm_mode = True
