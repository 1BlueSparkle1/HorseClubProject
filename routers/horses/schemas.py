from datetime import date

from pydantic import BaseModel, ConfigDict


class HorseBase(BaseModel):
    moniker: str
    birthday: date


class HorseCreate(HorseBase):
    pass


class HorseUpdate(HorseCreate):
    pass


class HorseUpdatePartial(HorseCreate):
    moniker: str | None = None
    birthday: date | None = None


class Horse(HorseBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
