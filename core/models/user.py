from typing import TYPE_CHECKING
from datetime import date
from sqlalchemy.orm import Mapped, relationship, mapped_column
from .base import Base

if TYPE_CHECKING:
    from .order import Order


class User(Base):
    surname: Mapped[str]
    name: Mapped[str]
    birthday: Mapped[date]
    login: Mapped[str] = mapped_column(unique=True)
    password: Mapped[bytes]
    role: Mapped[str]

    orders: Mapped[list["Order"]] = relationship(back_populates="user")
