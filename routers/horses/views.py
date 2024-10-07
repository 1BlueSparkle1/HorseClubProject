from fastapi import (
    APIRouter,
    status,
    HTTPException,
)
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_pagination import (
    Params,
    Page,
    paginate,
)

from auth.jwt_auth import get_current_auth_user
from .dependencies import horse_by_id
from core.models import db_helper, User
from . import crud
from .schemas import (
    Horse,
    HorseCreate,
    HorseUpdate,
    HorseUpdatePartial,
)

router = APIRouter(tags=["Horses"])


@router.get("/", response_model=Page[Horse])
async def get_horses(
    session: AsyncSession = Depends(db_helper.session_dependency),
    params: Params = Depends(),
):
    horses = await crud.get_horses(session=session)
    return paginate(horses, params)


@router.post(
    "/",
    response_model=Horse,
    status_code=status.HTTP_201_CREATED,
)
async def create_horse(
    horse_in: HorseCreate,
    session: AsyncSession = Depends(db_helper.session_dependency),
    user_me: User = Depends(get_current_auth_user),
):
    if user_me.role.lower() == "admin":
        return await crud.create_horse(session=session, horse_in=horse_in)
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Insufficient user rights.",
    )


@router.get("/{horse_id}", response_model=Horse)
async def get_horse(
    horse: Horse = Depends(horse_by_id),
):
    return horse


@router.put("/{horse_id}/")
async def update_horse(
    horse_update: HorseUpdate,
    horse: Horse = Depends(horse_by_id),
    session: AsyncSession = Depends(db_helper.session_dependency),
    user_me: User = Depends(get_current_auth_user),
):
    if user_me.role.lower() == "admin":
        return await crud.update_horse(
            session=session,
            horse=horse,
            horse_update=horse_update,
        )
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Insufficient user rights.",
    )


@router.patch("/{horse_id}/")
async def update_horse_partial(
    horse_update: HorseUpdatePartial,
    horse: Horse = Depends(horse_by_id),
    session: AsyncSession = Depends(db_helper.session_dependency),
    user_me: User = Depends(get_current_auth_user),
):
    if user_me.role.lower() == "admin":
        return await crud.update_horse(
            session=session,
            horse=horse,
            horse_update=horse_update,
            partial=True,
        )
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Insufficient user rights.",
    )


@router.delete(
    "/{horse_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_horse(
    horse: Horse = Depends(horse_by_id),
    session: AsyncSession = Depends(db_helper.session_dependency),
    user_me: User = Depends(get_current_auth_user),
) -> None:
    if user_me.role.lower() == "admin":
        await crud.delete_horse(
            session=session,
            horse=horse,
        )
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Insufficient user rights.",
    )
