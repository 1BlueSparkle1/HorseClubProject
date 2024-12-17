from contextlib import asynccontextmanager

from fastapi import FastAPI

import uvicorn

from appForms.app_horse import MyHorseForm, ListHorseForm
from appForms.app_orders import MyOrderForm, ListOrderForm
from appForms.app_users import MyUserForm, ListUserForm
from core.models import db_helper
from lib.fast_gui import App
from routers import router as router_v1
from auth.jwt_auth import router as router_jwt




@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(title="Horse Club", lifespan=lifespan)
app.include_router(router=router_v1)
app.include_router(router=router_jwt)

form_app = App(db=db_helper.session_dependency, custom_forms=[MyUserForm, MyHorseForm, MyOrderForm, ListUserForm, ListHorseForm, ListOrderForm])

app.mount("/forms/", form_app.app)


@app.get("/")
def hello_index():
    return {
        "message": "Hello index!",
    }


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
