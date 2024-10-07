from fastapi import (
    APIRouter,
    Depends,
    Form,
    HTTPException,
    status,
)
from pydantic import BaseModel
from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials,
    OAuth2PasswordBearer,
)
from auth import utils as auth_utils
from core.models import User, db_helper
from jwt.exceptions import InvalidTokenError

from routers.users import crud
from routers.users.schemas import UserCreate

http_bearer = HTTPBearer()
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/jwt/login/")


class TokenInfo(BaseModel):
    access_token: str
    token_type: str


router = APIRouter(prefix="/jwt", tags=["JWT"])


async def get_user(login: str, session: AsyncSession) -> User:
    # print(type(session))
    stmt = select(User).where(User.login == login)
    result: Result = await session.execute(stmt)
    user = result.scalars().first()
    return user


async def validate_auth_user(
    login: str = Form(),
    password: str = Form(),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid username or password",
    )
    # print(type(session))
    try:
        user = await get_user(login, session)
    except Exception as exc:
        raise exc
    # print(user)
    if not user:
        raise unauthed_exc

    if auth_utils.validate_password(
        password=password,
        hashed_password=user.password,
    ):
        return user

    raise unauthed_exc


def get_current_token_payload(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
    # token: str = Depends(oauth2_scheme),
):
    token = credentials.credentials
    print(token)
    try:
        payload = auth_utils.decode_jwt(
            token=token,
        )
    except InvalidTokenError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            # detail=f"invalid token error: {exc}",
            detail=f"invalid token error",
        )
    return payload


async def get_current_auth_user(
    payload: dict = Depends(get_current_token_payload),
    session: AsyncSession = Depends(
        db_helper.session_dependency,
    ),
) -> User:
    login: str | None = payload.get("login")
    try:
        user = await get_user(login, session)
        return user
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="token invalid",
        )


@router.post("/login/", response_model=TokenInfo)
def auth_user_issue_jwt(
    user: User = Depends(validate_auth_user),
):
    jwt_payload = {
        "sub": user.id,
        "login": user.login,
        "role": user.role,
    }
    token = auth_utils.encode_jwt(jwt_payload)
    return TokenInfo(
        access_token=token,
        token_type="Bearer",
    )


@router.get("/user/me/")
def auth_user_check_self_info(
    payload: dict = Depends(get_current_token_payload),
    user: User = Depends(get_current_auth_user),
):
    iat = payload.get("iat")
    return {
        "login": user.login,
        "role": user.role,
        "logged_in_at": iat,
    }


@router.post("/registration/")
async def reg_user_profile(
    user_in: UserCreate,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.create_user(session=session, user_in=user_in)
