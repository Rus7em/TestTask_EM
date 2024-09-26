from pydantic import BaseModel


class CreateProduct(BaseModel):
    name: str
    description: str
    price: float
    num: int


class ReadProduct(BaseModel):
    id: int
    name: str
    description: str
    price: float
    num: int

    class Config:
        from_attributes = True
