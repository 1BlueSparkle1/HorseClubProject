from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from lib.fast_gui import App, GroupConfig, Form
from core.models.horse import Horse
from lib.fast_gui.src import elements
from lib.fast_gui.src.form import requisites

from routers.horses.schemas import HorseBase, HorseCreate, HorseUpdate


# horse_group = GroupConfig(
#     db_model=Horse,
#     name='horses',
#     title='Лошади',
#     schema=HorseBase,
#     prefix='horses_form',
#     list_pagination='pages'
# )
#
#
# app_horse = App(
#     db=db_helper.session_dependency,
#     groups=[horse_group],
#     custom_forms=[],
#     routers=[])

class ListHorseForm(Form):
    name = "list_horse_form"
    title = "Форма списка лошадей"
    path = "/form/horses"

    def create(self):
        list_req = self.create_requisite(requisites.RequisiteType.DYNAMIC_LIST, name="listHorseReq", data_from={"path": "/horses"}, requisites=[self.create_requisite(requisites.RequisiteType.NUMBER, name="id"), self.create_requisite(requisites.RequisiteType.TEXT, name="moniker"), self.create_requisite(requisites.RequisiteType.DATETIME, name="birth")])
        self.add_requisite([list_req])

        horse_list = self.create_element(elements.ElementTypes.DYNAMIC_LIST, requisite=list_req, name="listHorseEl")
        self.add_element([horse_list])



class MyHorseForm(Form):
    name = "horse_form"
    title = "Форма для лошади"
    path = "/form/horse"

    def create(self):
        req_id = self.create_requisite(requisites.RequisiteType.NUMBER, name="idHorse")
        reg_moniker = self.create_requisite(requisites.RequisiteType.TEXT, name="horseM")
        reg_birth = self.create_requisite(requisites.RequisiteType.DATETIME, name="horseB")
        reg_status = self.create_requisite(requisites.RequisiteType.TEXT, name="status")
        self.add_requisite([req_id, reg_moniker, reg_birth])

        id_el = self.create_element(elements.ElementTypes.TEXT_INPUT, name="id", requisite=req_id, events={"on_change": self.action_function}, title="id")
        horse_moniker = self.create_element(elements.ElementTypes.TEXT_INPUT, name="horseTextM", requisite=reg_moniker, title="Кличка")
        horse_birth = self.create_element(elements.ElementTypes.TEXT_INPUT, name="horseTextB", requisite=reg_birth, title="Дата рождения")

        status_el = self.create_element(elements.ElementTypes.TEXT, name="horseStatus", requisite=reg_status, title="Статус")
        but_new = self.create_element(elements.ElementTypes.BUTTON, name="horseNew", events={"on_press": self.action_function_new}, title="добавить лошадь")
        but_update = self.create_element(elements.ElementTypes.BUTTON, name="horseUpdate", events={"on_press": self.action_function_update}, title="Изменить лошадь")
        but_delete = self.create_element(elements.ElementTypes.BUTTON, name="horseDelete", events={"on_press": self.action_function_delete}, title="Удалить лошадь")
        self.add_element([id_el, horse_moniker, horse_birth, but_new, but_update, but_delete, status_el])

    async def action_function(form, db: AsyncSession):
        id_horse = form.get_element("id")
        horse_id = int(id_horse.value)

        horse_req_m = form.get_requisite("horseM")
        horse = await db.get(Horse, horse_id)
        horse_req_m.value = f"{horse.moniker}"
        horse_req_b = form.get_requisite("horseB")
        horse_req_b.value = f"{str(horse.birthday)}"

        return form

    async def action_function_new(form, db: AsyncSession):
        moniker_horse = form.get_element("horseTextM")
        birth_horse = form.get_element("horseTextB")

        horse_new: HorseCreate = HorseCreate()
        horse_new.moniker = moniker_horse.value
        horse_new.birthday = birth_horse.value
        horse = Horse(**horse_new.model_dump())
        db.add(horse)
        await db.commit()

        status_reg = form.get_requisite("status")
        status_reg.value = "Лошадь создана!"

        return form

    async def action_function_update(form, db: AsyncSession):
        id_horse = form.get_element("id")
        horse_id = int(id_horse.value)
        moniker_horse = form.get_element("horseTextM")
        birth_horse = form.get_element("horseTextB")

        horse = await db.get(Horse, horse_id)
        horse_update: HorseUpdate = HorseUpdate()
        horse_update.moniker = moniker_horse.value
        horse_update.birthday = birth_horse.value
        for name, value in horse_update.model_dump(exclude_unset=False).items():
            setattr(horse, name, value)
        await db.commit()

        status_reg = form.get_requisite("status")
        status_reg.value = "Лошадь изменена!"

        return form

    async def action_function_delete(form, db: AsyncSession):
        id_horse = form.get_element("id")
        horse_id = int(id_horse.value)
        horse = await db.get(Horse, horse_id)

        await db.delete(horse)
        await db.commit()

        status_reg = form.get_requisite("status")
        status_reg.value = "Лошадь Удалена!"

        return form

