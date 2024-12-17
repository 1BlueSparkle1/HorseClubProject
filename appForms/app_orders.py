from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from lib.fast_gui import App, GroupConfig, Form
from core.models.order import Order
from lib.fast_gui.src import elements
from lib.fast_gui.src.form import requisites
from routers.orders.schemas import OrderBase, OrderCreate, OrderUpdate


# order_group = GroupConfig(
#     db_model=Order,
#     name='orders',
#     title='Записи',
#     schema=OrderBase,
#     prefix='orders_form',
#     list_pagination='pages'
# )
#
#
# app_order = App(db=db_helper.session_dependency, groups=[order_group])

class ListOrderForm(Form):
    name = "list_order_form"
    title = "Форма списка записей"
    path = "/form/orders"

    def create(self):
        list_req = self.create_requisite(requisites.RequisiteType.DYNAMIC_LIST, name="listOrderReq",
                                         data_from={"path": "/orders"},
                                         requisites=[self.create_requisite(requisites.RequisiteType.NUMBER, name="id"),
                                                     self.create_requisite(requisites.RequisiteType.DATETIME, name="dateCreate"),
                                                     self.create_requisite(requisites.RequisiteType.DATETIME, name="orderDate"),
                                                     self.create_requisite(requisites.RequisiteType.TEXT, name="status"),
                                                     self.create_requisite(requisites.RequisiteType.NUMBER, name="idHorse"),
                                                     self.create_requisite(requisites.RequisiteType.NUMBER, name="idUser")])
        self.add_requisite([list_req])

        order_list = self.create_element(elements.ElementTypes.DYNAMIC_LIST, requisite=list_req, name="listOrderEl")
        self.add_element([order_list])



class MyOrderForm(Form):
    name = "order_form"
    title = "Форма для Записи"
    path = "/form/order"

    def create(self):
        req_id = self.create_requisite(requisites.RequisiteType.NUMBER, name="idOrder")
        reg_date_create = self.create_requisite(requisites.RequisiteType.DATETIME, name="orderCreate")
        reg_date_order = self.create_requisite(requisites.RequisiteType.DATETIME, name="orderDate")
        reg_status_order = self.create_requisite(requisites.RequisiteType.TEXT, name="orderStatus")
        req_id_horse = self.create_requisite(requisites.RequisiteType.NUMBER, name="idHorse")
        req_id_user = self.create_requisite(requisites.RequisiteType.NUMBER, name="idUser")
        reg_status = self.create_requisite(requisites.RequisiteType.TEXT, name="status")
        self.add_requisite([req_id, reg_date_create, reg_date_order, reg_status_order, req_id_horse, req_id_user, reg_status])

        id_el = self.create_element(elements.ElementTypes.TEXT_INPUT, name="id", requisite=req_id, events={"on_change": self.action_function}, title="id")
        order_create = self.create_element(elements.ElementTypes.TEXT_INPUT, name="orderTextC", requisite=reg_date_create, title="Дата создания записи")
        order_date = self.create_element(elements.ElementTypes.TEXT_INPUT, name="orderTextD", requisite=reg_date_order, title="Дата записи")
        order_status = self.create_element(elements.ElementTypes.TEXT, name="orderStatus", requisite=reg_status_order, title="Статус записи")
        id_horse = self.create_element(elements.ElementTypes.TEXT_INPUT, name="horseId", requisite=req_id_horse, title="id лошади")
        id_user = self.create_element(elements.ElementTypes.TEXT_INPUT, name="userId", requisite=req_id_user, title="id клиента")

        status_el = self.create_element(elements.ElementTypes.TEXT, name="statusOrder", requisite=reg_status, title="Статус")
        but_new = self.create_element(elements.ElementTypes.BUTTON, name="orderNew", events={"on_press": self.action_function_new}, title="добавить запись")
        but_update = self.create_element(elements.ElementTypes.BUTTON, name="orderUpdate", events={"on_press": self.action_function_update}, title="Изменить запись")
        but_delete = self.create_element(elements.ElementTypes.BUTTON, name="orderDelete", events={"on_press": self.action_function_delete}, title="Удалить запись")
        self.add_element([id_el, order_create, order_date, order_status, id_horse, id_user, but_new, but_update, but_delete, status_el])

    async def action_function(form, db: AsyncSession):
        id_order = form.get_element("id")
        order_id = int(id_order.value)

        order_req_c = form.get_requisite("orderCreate")
        order = await db.get(Order, order_id)
        order_req_c.value = f"{order.date_create}"
        order_req_o = form.get_requisite("orderDate")
        order_req_o.value = f"{order.date_order}"
        order_req_s = form.get_requisite("orderStatus")
        order_req_s.value = f"{order.status}"
        order_req_h = form.get_requisite("idHorse")
        order_req_h.value = f"{order.horse_id}"
        order_req_u = form.get_requisite("idUser")
        order_req_u.value = f"{order.user_id}"

        return form

    async def action_function_new(form, db: AsyncSession):
        create_order = form.get_element("orderCreate")
        date_order = form.get_element("orderDate")
        status_order = form.get_element("orderStatus")
        id_horse = form.get_element("idHorse")
        id_user = form.get_element("idUser")

        order_new: OrderCreate = OrderCreate()
        order_new.date_create = create_order.value
        order_new.date_order = date_order.value
        order_new.status = status_order.value
        order_new.horse_id = id_horse.value
        order_new.user_id = id_user.value
        order = Order(**order_new.model_dump())
        db.add(order)
        await db.commit()

        status_reg = form.get_requisite("status")
        status_reg.value = "Запись создана!"

        return form

    async def action_function_update(form, db: AsyncSession):
        id_order = form.get_element("id")
        order_id = int(id_order.value)
        create_order = form.get_element("orderCreate")
        date_order = form.get_element("orderDate")
        status_order = form.get_element("orderStatus")
        id_horse = form.get_element("idHorse")
        id_user = form.get_element("idUser")

        order = await db.get(Order, order_id)
        order_update: OrderUpdate = OrderUpdate()
        order_update.date_create = create_order.value
        order_update.date_order = date_order.value
        order_update.status = status_order.value
        order_update.horse_id = id_horse.value
        order_update.user_id = id_user.value
        for name, value in order_update.model_dump(exclude_unset=False).items():
            setattr(order, name, value)
        await db.commit()

        status_reg = form.get_requisite("status")
        status_reg.value = "Запись изменена!"

        return form

    async def action_function_delete(form, db: AsyncSession):
        id_order = form.get_element("id")
        order_id = int(id_order.value)
        order= await db.get(Order, order_id)

        await db.delete(order)
        await db.commit()

        status_reg = form.get_requisite("status")
        status_reg.value = "Запись Удалена!"

        return form