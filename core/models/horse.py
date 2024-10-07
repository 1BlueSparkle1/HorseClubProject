from datetime import date
from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, relationship
from .base import Base

if TYPE_CHECKING:
    from .order import Order


class Horse(Base):
    moniker: Mapped[str]
    birthday: Mapped[date]

    orders: Mapped[list["Order"]] = relationship(back_populates="horse")
