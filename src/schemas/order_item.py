from pydantic import BaseModel


class CreateOrderItem(BaseModel):
    product_id: int
    num: int
