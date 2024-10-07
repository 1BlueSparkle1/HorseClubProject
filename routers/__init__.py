from fastapi import APIRouter

from .horses.views import router as horses_router
from .users.views import router as user_router
from .orders.views import router as order_router

router = APIRouter()
router.include_router(router=horses_router, prefix="/horses")
router.include_router(router=user_router, prefix="/users")
router.include_router(router=order_router, prefix="/orders")
