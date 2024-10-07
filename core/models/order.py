from typing import TYPE_CHECKING
from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, MappedColumn, relationship
from .base import Base

if TYPE_CHECKING:
    from .user import User
    from .horse import Horse


class Order(Base):
    date_create: Mapped[datetime]
    date_order: Mapped[datetime]
    status: Mapped[str]
    horse_id: Mapped[int] = MappedColumn(
        ForeignKey("horses.id"),
    )
    user_id: Mapped[int] = MappedColumn(
        ForeignKey("users.id"),
    )
    user: Mapped["User"] = relationship(back_populates="orders")
    horse: Mapped["Horse"] = relationship(back_populates="orders")
