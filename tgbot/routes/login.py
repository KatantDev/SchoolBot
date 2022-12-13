from aiohttp.web_fileresponse import FileResponse
from aiohttp.web_request import Request
from aiohttp.web_response import json_response

from aiogram import Bot
from aiogram.utils.web_app import check_webapp_signature, safe_parse_webapp_init_data

import localization
from nschool import NetSchoolAPI, errors
from tgbot.database import Users
from tgbot.keyboards import default


async def get_student(login, password):
    api = NetSchoolAPI('https://sgo.prim-edu.ru/')
    student = await api.login(
        login,
        password,
        'МБОУ \"СОШ № 60\"'
    )
    await api.logout()
    return student


async def login_handler(request: Request):
    return FileResponse("login.html")


async def check_data_handler(request: Request):
    bot: Bot = request.app["bot"]

    data = await request.post()
    if check_webapp_signature(bot.token, data["_auth"]):
        return json_response({"ok": True})
    return json_response({"ok": False, "payload": "Unauthorized"}, status=401)


async def send_message_handler(request: Request):
    bot: Bot = request.app["bot"]
    data = await request.post()

    try:
        web_app_init_data = safe_parse_webapp_init_data(token=bot.token, init_data=data["_auth"])
    except ValueError:
        return json_response({"ok": False, "payload": "Unauthorized"}, status=401)

    try:
        await get_student(data['login'], data['password'])
        user = await Users.filter(user_id=data['user_id']).first()
        user.login = data['login']
        user.password = data['password']
        user.status = 'student'
        await user.save()

        await bot.send_message(
            data['user_id'],
            localization.signed_in,
            reply_markup=default.main.as_markup(resize_keyboard=True)
        )
        return json_response({"ok": True})
    except errors.AuthError:
        return json_response({"ok": False, "payload": localization.incorrect_password})
