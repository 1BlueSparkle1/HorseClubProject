from fastapi import FastAPI
from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from auth.utils import hash_password
from core.models import db_helper
from lib.fast_gui import App, GroupConfig, Form
from core.models.user import User
from lib.fast_gui.src import form, elements
from lib.fast_gui.src.form import requisites
from routers.users.schemas import UserBase, UserCreate, UserUpdate


# user_group = GroupConfig(
#     db_model=User,
#     name='users',
#     title='Пользователи',
#     schema=UserBase,
#     prefix='users_form',
#     list_pagination='pages'
# )
#
#
# app_user = App(db=db_helper.session_dependency, groups=[user_group])


# class MyUserForm(Form):
#     name = "user_all_form"
#     title = "Все пользователи"
#     path = "/app_user/all"
#
#     def create(self):
#         req_list = self.create_requisite(requisites.RequisiteType.LIST, name="listUser")
#         self.add_requisite(req_list)
#
#         element = self.create_element(elements.ElementTypes.BUTTON, name="Output", title="Кнопка", events={"on_press": self.action_function})
#         self.add_element(element)
#
#     async def action_function(form, db: AsyncSession):
#         stmt = select(User).order_by(User.id)
#         result: Result = await db.execute(stmt)
#         user = result.scalars().all()
#         list_req = form.get_requisite("listUser")
#         list_req.value = list(user)
#
#         return form

class ListUserForm(Form):
    name = "list_user_form"
    title = "Форма списка пользователей"
    path = "/form/users"

    def create(self):
        list_req = self.create_requisite(requisites.RequisiteType.DYNAMIC_LIST, name="listUserReq",
                                         data_from={"path": "/users"},
                                         requisites=[self.create_requisite(requisites.RequisiteType.NUMBER, name="id"),
                                                     self.create_requisite(requisites.RequisiteType.TEXT, name="surname"),
                                                     self.create_requisite(requisites.RequisiteType.TEXT, name="name"),
                                                     self.create_requisite(requisites.RequisiteType.DATETIME, name="birth"),
                                                     self.create_requisite(requisites.RequisiteType.TEXT, name="role"),
                                                     self.create_requisite(requisites.RequisiteType.TEXT, name="login"),
                                                     self.create_requisite(requisites.RequisiteType.TEXT, name="password")])
        self.add_requisite([list_req])

        user_list = self.create_element(elements.ElementTypes.DYNAMIC_LIST, requisite=list_req, name="listUserEl")
        self.add_element([user_list])



class MyUserForm(Form):
    name = "user_form"
    title = "Форма для пользователя"
    path = "/form/user"

    def create(self):
        req_id = self.create_requisite(requisites.RequisiteType.NUMBER, name="idUser")
        reg_surname = self.create_requisite(requisites.RequisiteType.TEXT, name="userS")
        reg_name = self.create_requisite(requisites.RequisiteType.TEXT, name="userN")
        reg_birthday = self.create_requisite(requisites.RequisiteType.DATETIME, name="userB")
        reg_role = self.create_requisite(requisites.RequisiteType.TEXT, name="userR")
        reg_login = self.create_requisite(requisites.RequisiteType.TEXT, name="userL")
        reg_password = self.create_requisite(requisites.RequisiteType.TEXT, name="userP")
        reg_status = self.create_requisite(requisites.RequisiteType.TEXT, name="status")
        self.add_requisite([req_id, reg_surname, reg_name, reg_birthday, reg_role, reg_login, reg_password, reg_status])

        text_el = self.create_element(elements.ElementTypes.TEXT_INPUT, name="id", requisite=req_id, events={"on_change": self.action_function}, title="id")
        user_surname = self.create_element(elements.ElementTypes.TEXT_INPUT, name="userTextS", requisite=reg_surname, title="Фамилия")
        user_name = self.create_element(elements.ElementTypes.TEXT_INPUT, name="userTextN", requisite=reg_name, title="Имя")
        user_birthday = self.create_element(elements.ElementTypes.TEXT_INPUT, name="userTextB", requisite=reg_birthday, title="Дата рождения")
        user_role = self.create_element(elements.ElementTypes.TEXT_INPUT, name="userTextR", requisite=reg_role, title="Роль")
        user_login = self.create_element(elements.ElementTypes.TEXT_INPUT, name="userTextL", requisite=reg_login, title="Логин")
        user_password = self.create_element(elements.ElementTypes.TEXT_INPUT, name="userTextP", requisite=reg_password, title="Пароль")

        status_el = self.create_element(elements.ElementTypes.TEXT, name="userStatus", requisite=reg_status, title="Статус")
        but_new = self.create_element(elements.ElementTypes.BUTTON, name="userNew", events={"on_press": self.action_function_new}, title="добавить пользователя")
        but_update = self.create_element(elements.ElementTypes.BUTTON, name="userUpdate", events={"on_press": self.action_function_update}, title="Изменить пользователя")
        but_delete = self.create_element(elements.ElementTypes.BUTTON, name="userDelete", events={"on_press": self.action_function_delete}, title="Удалить пользователя")
        self.add_element([text_el, user_surname, user_name, user_birthday, user_role, user_login, user_password, but_new, but_update, but_delete, status_el])

    async def action_function(form, db: AsyncSession):
        id_user = form.get_element("id")
        user_id = int(id_user.value)

        user_req_s = form.get_requisite("userS")
        user = await db.get(User, user_id)
        user_req_s.value = f"{user.surname}"
        user_req_n = form.get_requisite("userN")
        user_req_n.value = f"{user.name}"
        user_req_b = form.get_requisite("userB")
        user_req_b.value = f"{user.birthday}"
        user_req_r = form.get_requisite("userR")
        user_req_r.value = f"{user.role}"
        user_req_l = form.get_requisite("userL")
        user_req_l.value = f"{user.login}"
        user_req_p = form.get_requisite("userP")
        user_req_p.value = f"{str(user.password)}"

        return form

    async def action_function_new(form, db: AsyncSession):
        sur_user = form.get_element("userTextS")
        name_user = form.get_element("userTextN")
        birth_user = form.get_element("userTextB")
        role_user = form.get_element("userTextR")
        log_user = form.get_element("userTextL")
        pass_user = form.get_element("userTextP")

        user_new : UserCreate = UserCreate()
        user_new.surname = sur_user.value
        user_new.name = name_user.value
        user_new.birthday = birth_user.value
        user_new.role = role_user.value
        user_new.login = log_user.value
        user_new.password = hash_password(pass_user)
        user = User(**user_new.model_dump())
        db.add(user)
        await db.commit()

        status_reg = form.get_requisite("status")
        status_reg.value = "Пользовать создан!"

        return form

    async def action_function_update(form, db: AsyncSession):
        id_user = form.get_element("id")
        user_id = int(id_user.value)
        sur_user = form.get_element("userTextS")
        name_user = form.get_element("userTextN")
        birth_user = form.get_element("userTextB")
        role_user = form.get_element("userTextR")
        log_user = form.get_element("userTextL")
        pass_user = form.get_element("userTextP")

        user = await db.get(User, user_id)
        user_update : UserUpdate = UserUpdate()
        user_update.surname = sur_user.value
        user_update.name = name_user.value
        user_update.birthday = birth_user.value
        user_update.role = role_user.value
        user_update.login = log_user.value
        user_update.password = hash_password(pass_user)
        for name, value in user_update.model_dump(exclude_unset=False).items():
            setattr(user, name, value)
        await db.commit()

        status_reg = form.get_requisite("status")
        status_reg.value = "Пользовать изменен!"

        return form

    async def action_function_delete(form, db: AsyncSession):
        id_user = form.get_element("id")
        user_id = int(id_user.value)
        user = await db.get(User, user_id)

        await db.delete(user)
        await db.commit()

        status_reg = form.get_requisite("status")
        status_reg.value = "Пользовать Удален!"

        return form
