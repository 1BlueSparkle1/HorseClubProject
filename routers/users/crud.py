from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from auth.utils import hash_password
from core.models import User

from routers.users.schemas import (
    UserCreate,
    UserUpdate,
    UserUpdatePartial,
)


async def get_users(
    session: AsyncSession,
) -> list[User]:
    stmt = select(User).order_by(User.id)
    result: Result = await session.execute(stmt)
    horses = result.scalars().all()

    return list(horses)


async def get_user(session: AsyncSession, user_id: int) -> User | None:
    return await session.get(User, user_id)


async def create_user(session: AsyncSession, user_in: UserCreate) -> User:
    # user_hash: UserCreateHash = UserCreateHash()
    # user_hash = await hash_password.create_user_hash(user_in, user_hash)
    user_in.password = hash_password(user_in.password)
    user = User(**user_in.model_dump())
    session.add(user)
    await session.commit()
    # await session.refresh(user)
    return user


async def update_user(
    session: AsyncSession,
    user: User,
    user_update: UserUpdate | UserUpdatePartial,
    partial: bool = False,
) -> User:
    user_update.password = hash_password(user_update.password)
    for name, value in user_update.model_dump(exclude_unset=partial).items():
        setattr(user, name, value)
    # user.password = hash_password(user.password)
    await session.commit()
    return user


async def delete_user(
    session: AsyncSession,
    user: User,
) -> None:
    await session.delete(user)
    await session.commit()
