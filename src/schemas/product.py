from pydantic import BaseModel, ConfigDict


class CreateProduct(BaseModel):
    name: str
    description: str
    price: float
    num: int


class ReadProduct(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str
    price: float
    num: int

