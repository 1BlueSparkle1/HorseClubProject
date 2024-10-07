from fastapi import (
    APIRouter,
    status,
    HTTPException,
)
from fastapi.params import Depends
from fastapi_pagination import Params, Page, paginate
from sqlalchemy.ext.asyncio import AsyncSession

from auth.jwt_auth import get_current_auth_user
from .dependencies import user_by_id
from core.models import db_helper
from . import crud
from .schemas import (
    User,
    UserCreate,
    UserUpdate,
    UserUpdatePartial,
)

router = APIRouter(tags=["Users"])


@router.get("/", response_model=Page[User])
async def get_users(
    user_me: User = Depends(get_current_auth_user),
    session: AsyncSession = Depends(db_helper.session_dependency),
    params: Params = Depends(),
):
    if user_me.role.lower() == "admin":
        users = await crud.get_users(session=session)
        return paginate(users, params)
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Insufficient user rights.",
    )


@router.post(
    "/",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    user_in: UserCreate,
    user_me: User = Depends(get_current_auth_user),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    if user_me.role.lower() == "admin":
        return await crud.create_user(session=session, user_in=user_in)
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Insufficient user rights.",
    )


@router.get("/{user_id}", response_model=User)
async def get_user(
    user_me: User = Depends(get_current_auth_user),
    user: User = Depends(user_by_id),
):
    if user_me.role.lower() == "admin" or user_me.id == user.id:
        return user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Insufficient user rights.",
    )


@router.put("/{user_id}/")
async def update_user(
    user_update: UserUpdate,
    user: User = Depends(user_by_id),
    user_me: User = Depends(get_current_auth_user),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    if user_me.role.lower() == "admin" or user_me.id == user.id:
        return await crud.update_user(
            session=session,
            user=user,
            user_update=user_update,
        )
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Insufficient user rights.",
    )


@router.patch("/{user_id}/")
async def update_user_partial(
    user_update: UserUpdatePartial,
    user: User = Depends(user_by_id),
    user_me: User = Depends(get_current_auth_user),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    if user_me.role.lower() == "admin" or user_me.id == user.id:
        return await crud.update_user(
            session=session,
            user=user,
            user_update=user_update,
            partial=True,
        )
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Insufficient user rights.",
    )


@router.delete(
    "/{user_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_user(
    user: User = Depends(user_by_id),
    user_me: User = Depends(get_current_auth_user),
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> None:
    if user_me.role.lower() == "admin":
        await crud.delete_user(
            session=session,
            user=user,
        )
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Insufficient user rights.",
    )
