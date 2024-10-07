from contextlib import asynccontextmanager

from fastapi import FastAPI

import uvicorn

from routers import router as router_v1
from auth.jwt_auth import router as router_jwt


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(title="Horse Club", lifespan=lifespan)
app.include_router(router=router_v1)
app.include_router(router=router_jwt)


@app.get("/")
def hello_index():
    return {
        "message": "Hello index!",
    }


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
