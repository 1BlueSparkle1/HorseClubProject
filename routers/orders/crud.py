from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import Order
from routers.orders.schemas import OrderCreate, OrderUpdate, OrderUpdatePartial


async def get_orders(session: AsyncSession) -> list[Order]:
    stmt = select(Order).order_by(Order.id)
    result: Result = await session.execute(stmt)
    orders = result.scalars().all()
    return list(orders)


async def get_order(session: AsyncSession, order_id: int) -> Order | None:
    return await session.get(Order, order_id)


async def create_order(session: AsyncSession, order_in: OrderCreate) -> Order:
    order = Order(**order_in.model_dump())
    session.add(order)
    await session.commit()
    # await session.refresh(horse)
    return order


async def create_my_order(
    session: AsyncSession, order_in: OrderCreate, user_id: int
) -> Order:
    order = Order(**order_in.model_dump())
    order.user_id = user_id
    session.add(order)
    await session.commit()
    # await session.refresh(horse)
    return order


async def update_order(
    session: AsyncSession,
    order: Order,
    order_update: OrderUpdate | OrderUpdatePartial,
    partial: bool = False,
) -> Order:
    for name, value in order_update.model_dump(exclude_unset=partial).items():
        setattr(order, name, value)
    await session.commit()
    return order


async def update_my_order(
    session: AsyncSession,
    order: Order,
    order_update: OrderUpdatePartial,
    user_id: int,
    partial: bool = False,
) -> Order:
    for name, value in order_update.model_dump(exclude_unset=partial).items():
        setattr(order, name, value)
        order.user_id = user_id
    await session.commit()
    return order


async def delete_order(
    session: AsyncSession,
    order: Order,
) -> None:
    await session.delete(order)
    await session.commit()
