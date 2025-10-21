from typing import Optional

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class HotelsTable(Base):
    __tablename__ = "hotels"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created_at: Mapped[str] = mapped_column(
        String(255), server_default="CURRENT_TIMESTAMP"
    )
    title: Mapped[str] = mapped_column(String(255))
    location: Mapped[Optional[str]] = mapped_column(String(255))
    rooms: Mapped[Optional[int]] = mapped_column()
