from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

from database import Base


class Status(Base):
    __tablename__ = "status"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
