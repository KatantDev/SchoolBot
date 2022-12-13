from aiogram.types import WebAppInfo

import localization
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from .callback import *
from .. import config

welcome = InlineKeyboardBuilder()
for start_key, start_value in localization.welcome['start_buttons'].items():
    welcome.add(
        InlineKeyboardButton(
            text=start_value,
            callback_data=WelcomeCb(type=start_key).pack()
        )
    )
welcome.adjust(1)


school_link = InlineKeyboardBuilder()
school_link.add(
    InlineKeyboardButton(
        text=localization.school_link[0],
        url=localization.school_link[1]
    )
)

inst_link = InlineKeyboardBuilder()
inst_link.add(
    InlineKeyboardButton(
        text=localization.inst_link[0],
        url=localization.inst_link[1]
    )
)

dnevnik_link = InlineKeyboardBuilder()
dnevnik_link.add(
    InlineKeyboardButton(
        text=localization.dnevnik_link[0],
        url=localization.dnevnik_link[1]
    )
)


login_keyboard = InlineKeyboardBuilder()
login_keyboard.add(
    InlineKeyboardButton(
        text=localization.student_login_button,
        web_app=WebAppInfo(url=f'{config.APP_BASE_URL}/login')
    )
)
login_keyboard.add(
    InlineKeyboardButton(
        text=localization.return_main[1],
        callback_data=WelcomeCb(type=localization.return_main[0]).pack()
    )
)
login_keyboard.adjust(1)


return_main = InlineKeyboardBuilder()
return_main.add(
    InlineKeyboardButton(
        text=localization.return_main[1],
        callback_data=WelcomeCb(type=localization.return_main[0]).pack()
    )
)

choose_date = InlineKeyboardBuilder()
for diary_key, diary_value in localization.diary_menu.items():
    choose_date.add(
        InlineKeyboardButton(
            text=diary_value,
            callback_data=ChooseDateCb(date=diary_key).pack()
        )
    )
choose_date.adjust(3)


def switch_diary(diary_type, date):
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(
            text=localization.switch_diary[diary_type],
            callback_data=SwitchDiaryCb(type=diary_type, date=date).pack()
        )
    )
    return keyboard


detail_marks = InlineKeyboardBuilder()
detail_marks.add(
    InlineKeyboardButton(
        text=localization.detail_marks[1],
        callback_data=MarksCb(type=localization.detail_marks[0]).pack()
    )
)

marks = InlineKeyboardBuilder()
marks.add(
    InlineKeyboardButton(
        text=localization.marks[1],
        callback_data=MarksCb(type=localization.marks[0]).pack()
    )
)
