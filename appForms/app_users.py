from fastapi import FastAPI
from core.models import db_helper
from lib.fast_gui import App, GroupConfig
from core.models.user import User
from routers.users.schemas import UserBase

user_group = GroupConfig(
    db_model=User,
    name='users',
    title='Пользователи',
    schema=UserBase,
    prefix='users_form',
    list_pagination='pages'
)


app_user = App(db=db_helper.session_dependency, groups=[user_group])


app = FastAPI()


app.mount("/appUser/", app_user.app)