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
from .dependencies import order_by_id
from core.models import db_helper, User
from . import crud
from .schemas import (
    Order,
    OrderCreate,
    OrderUpdate,
    OrderUpdatePartial,
)

router = APIRouter(tags=["Orders"])


@router.get("/", response_model=Page[Order])
async def get_orders(
    user_me: User = Depends(get_current_auth_user),
    session: AsyncSession = Depends(db_helper.session_dependency),
    params: Params = Depends(),
):
    if user_me.role.lower() == "admin":
        orders = await crud.get_orders(session=session)
        return paginate(orders, params)
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Insufficient user rights.",
    )


@router.get("/my_orders", response_model=Page[Order])
async def get_my_orders():
    pass


@router.post(
    "/",
    response_model=Order,
    status_code=status.HTTP_201_CREATED,
)
async def create_order(
    order_in: OrderCreate,
    user_me: User = Depends(get_current_auth_user),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    if user_me.role.lower() == "admin":
        return await crud.create_order(
            session=session,
            order_in=order_in,
        )
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Insufficient user rights.",
    )


@router.post(
    "my_order/",
    response_model=Order,
    status_code=status.HTTP_201_CREATED,
)
async def create_my_order(
    order_in: OrderCreate,
    user_me: User = Depends(get_current_auth_user),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.create_my_order(
        session=session,
        order_in=order_in,
        user_id=user_me.id,
    )


@router.get("/{order_id}", response_model=Order)
async def get_order(
    order: Order = Depends(order_by_id),
    user_me: User = Depends(get_current_auth_user),
):
    if user_me.role.lower() == "admin" or user_me.role.lower() == "manager":
        return order
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Insufficient user rights.",
    )


@router.get("my_order/{order_id}", response_model=Order)
async def get_order(
    order: Order = Depends(order_by_id),
    user_me: User = Depends(get_current_auth_user),
):
    if user_me.id == order.user_id:
        return order
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Order not found.",
    )


@router.put("/{order_id}/")
async def update_order(
    order_update: OrderUpdate,
    order: Order = Depends(order_by_id),
    user_me: User = Depends(get_current_auth_user),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    if user_me.role.lower() == "admin":
        return await crud.update_order(
            session=session,
            order=order,
            order_update=order_update,
        )
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Insufficient user rights.",
    )


@router.patch("/{order_id}/")
async def update_order_partial(
    order_update: OrderUpdatePartial,
    order: Order = Depends(order_by_id),
    session: AsyncSession = Depends(db_helper.session_dependency),
    user_me: User = Depends(get_current_auth_user),
):
    if user_me.role.lower() == "admin" or user_me.role.lower() == "manager":
        return await crud.update_order(
            session=session,
            order=order,
            order_update=order_update,
            partial=True,
        )
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Insufficient user rights.",
    )


@router.patch("my_orders/{order_id}/")
async def update_my_order_partial(
    order_update: OrderUpdatePartial,
    order: Order = Depends(order_by_id),
    session: AsyncSession = Depends(db_helper.session_dependency),
    user_me: User = Depends(get_current_auth_user),
):
    if user_me.id == order.user_id:
        return await crud.update_my_order(
            session=session,
            order=order,
            order_update=order_update,
            user_id=user_me.id,
            partial=True,
        )
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Order not found.",
    )


@router.delete(
    "/{order_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_order(
    order: Order = Depends(order_by_id),
    session: AsyncSession = Depends(db_helper.session_dependency),
    user_me: User = Depends(get_current_auth_user),
) -> None:
    if user_me.role.lower() == "admin":
        await crud.delete_order(
            session=session,
            order=order,
        )
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Insufficient user rights.",
    )
