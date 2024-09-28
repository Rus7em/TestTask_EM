from pydantic import BaseModel, ConfigDict


class CreateOrderItem(BaseModel):
    product_id: int
    num: int


class ReadOrderItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    order_id: int
    product_id: int
    num: int
