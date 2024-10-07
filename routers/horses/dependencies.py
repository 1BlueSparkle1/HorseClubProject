from typing import Annotated

from fastapi import (
    Path,
    Depends,
    HTTPException,
    status,
)
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper, Horse
from . import crud


async def horse_by_id(
    horse_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> Horse:
    horse = await crud.get_horse(session=session, horse_id=horse_id)
    if horse is not None:
        return horse
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Horse {horse_id} not found!"
    )
