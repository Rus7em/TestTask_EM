from pydantic import BaseModel, ConfigDict
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
    model_config = ConfigDict(from_attributes=True)
    id: int
    create_at: datetime
    status: Status
    items: Optional[List[ReadOrderItem]] = None

