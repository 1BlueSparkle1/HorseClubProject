from contextlib import asynccontextmanager

from fastapi import FastAPI

import uvicorn

from appForms.app_horse import app_horse
from appForms.app_orders import app_order
from appForms.app_users import app_user
from routers import router as router_v1
from auth.jwt_auth import router as router_jwt




@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(title="Horse Club", lifespan=lifespan)
app.include_router(router=router_v1)
app.include_router(router=router_jwt)

app.mount("/appHorse/", app_horse.app)
app.mount("/appUser/", app_user.app)
app.mount("/appOrder", app_order.app)


@app.get("/")
def hello_index():
    return {
        "message": "Hello index!",
    }


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
