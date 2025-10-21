from decimal import Decimal
from typing import Optional

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import mapped_column, Mapped

from database import Base


class RoomsTable(Base):
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id"))
    title: Mapped[str] = mapped_column(String(255))
    price: Mapped[Decimal] = mapped_column(String(255), default=0)
    description: Mapped[Optional[str]] = mapped_column()
    quantity: Mapped[int] = mapped_column(default=0)
