from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime, func, ForeignKey

from database import Base

class Order(Base):
    __tablename__ = "order"

    id: Mapped[int] = mapped_column(primary_key=True)
    create_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    status_id: Mapped[int] = mapped_column(ForeignKey("status.id"))

    class Config:
        orm_mode = True
