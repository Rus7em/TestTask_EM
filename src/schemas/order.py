from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from enum import StrEnum

from schemas.order_item import CreateOrderItem, ReadOrderItem


class Status(StrEnum):
    PROCESSING = "Processing"
    SHIPPED = "Shipped"
    DELIVERED = "Delivered"


class CreateOrder(BaseModel):
    state: Status
    items: List[CreateOrderItem]


class ReadOrder(BaseModel):
    id: int
    create_at: datetime
    status: Status
    items: Optional[List[ReadOrderItem]] = None

    class Config:
        from_attributes = True
