from pydantic import BaseModel
from typing import List

from order_item import CreateOrderItem


class CreateOrder(BaseModel):
    state: str
    items: List[CreateOrderItem]
