from fastapi import FastAPI
from core.models import db_helper
from lib.fast_gui import App, GroupConfig
from core.models.horse import Horse
from routers.horses.schemas import HorseBase

horse_group = GroupConfig(
    db_model=Horse,
    name='horses',
    title='Лошади',
    schema=HorseBase,
    prefix='horses_form',
    list_pagination='pages'
)


app_horse = App(
    db=db_helper.session_dependency,
    groups=[horse_group],
    custom_forms=[],
    routers=[])

app_cls = app_horse.app

app = FastAPI()

app.mount("/appHorse/", app_cls)


