import asyncio
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from nschool import NetSchoolAPI, errors

import localization
from localization import student_login
from tgbot.database import Users
from tgbot.keyboards import inline, default
from tgbot.states.states import Login


async def start(message: Message):
    await message.answer(localization.start_student, reply_markup=default.main.as_markup(resize_keyboard=True))


async def get_student(login, password):
    api = NetSchoolAPI('https://sgo.prim-edu.ru/')
    student = await api.login(
        login,
        password,
        'МБОУ \"СОШ № 60\"'
    )
    await api.logout()
    return student


async def enter_login(query: CallbackQuery, state: FSMContext):
    await query.message.edit_text(student_login, reply_markup=inline.login_keyboard.as_markup())


async def enter_password(message: Message, state: FSMContext):
    await state.update_data(login=message.text)
    await message.answer(student_login['enter_password'], reply_markup=inline.return_main.as_markup())
    await state.set_state(Login.password)


async def signed_in(message: Message, state: FSMContext):
    password = message.text
    data = await state.get_data()
    await state.clear()

    try:
        await get_student(data['login'], password)
        user = await Users.filter(user_id=message.from_user.id).first()
        user.login = data['login']
        user.password = password
        user.status = 'student'
        await user.save()

        await message.answer(student_login['signed_in'], reply_markup=default.main.as_markup())
    except errors.AuthError:
        await message.answer(student_login['incorrect_password'], reply_markup=inline.return_main.as_markup())

    await asyncio.sleep(5)
    await message.delete()
