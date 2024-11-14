from fastapi import FastAPI
from core.models import db_helper
from lib.fast_gui import App, GroupConfig
from core.models.order import Order
from routers.orders.schemas import OrderBase

order_group = GroupConfig(
    db_model=Order,
    name='orders',
    title='Записи',
    schema=OrderBase,
    prefix='orders_form',
    list_pagination='pages'
)


app_order = App(db=db_helper.session_dependency, groups=[order_group])


app = FastAPI()


app.mount("/appOrder", app_order.app)