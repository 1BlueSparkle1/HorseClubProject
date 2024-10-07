from datetime import datetime

from pydantic import BaseModel, ConfigDict


class OrderBase(BaseModel):
    date_create: datetime
    date_order: datetime
    status: str
    horse_id: int
    user_id: int


class OrderCreate(OrderBase):
    pass


class OrderUpdate(OrderCreate):
    pass


class OrderUpdatePartial(OrderCreate):
    date_create: datetime | None = None
    date_order: datetime | None = None
    status: str | None = None
    horse_id: int | None = None
    user_id: int | None = None


class Order(OrderBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
