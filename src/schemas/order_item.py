from pydantic import BaseModel


class CreateOrderItem(BaseModel):
    product_id: int
    num: int


class ReadOrderItem(BaseModel):
    id: int
    order_id: int
    product_id: int
    num: int

    class Config:
        from_attributes = True
