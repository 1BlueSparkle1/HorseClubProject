from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import Horse
from routers.horses.schemas import (
    HorseCreate,
    HorseUpdate,
    HorseUpdatePartial,
)


async def get_horses(session: AsyncSession) -> list[Horse]:
    stmt = select(Horse).order_by(Horse.id)
    result: Result = await session.execute(stmt)
    horses = result.scalars().all()
    return list(horses)


async def get_horse(session: AsyncSession, horse_id: int) -> Horse | None:
    return await session.get(Horse, horse_id)


async def create_horse(session: AsyncSession, horse_in: HorseCreate) -> Horse:
    horse = Horse(**horse_in.model_dump())
    session.add(horse)
    await session.commit()
    # await session.refresh(horse)
    return horse


async def update_horse(
    session: AsyncSession,
    horse: Horse,
    horse_update: HorseUpdate | HorseUpdatePartial,
    partial: bool = False,
) -> Horse:
    for name, value in horse_update.model_dump(exclude_unset=partial).items():
        setattr(horse, name, value)
    await session.commit()
    return horse


async def delete_horse(
    session: AsyncSession,
    horse: Horse,
) -> None:
    await session.delete(horse)
    await session.commit()
