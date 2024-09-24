from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

from database import Base


class Product(Base):
    __tablename__ = "product"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    description: Mapped[Optional[str]]
    price: Mapped[Optional[int]]
    num: Mapped[int]
