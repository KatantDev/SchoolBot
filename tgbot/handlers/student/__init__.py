from aiogram import Dispatcher, F
from aiogram.filters import StateFilter, Command

import localization
from tgbot.filters.chat_type import ChatType
from tgbot.filters.role import StudentFilter, GuestFilter
from .login import enter_login, enter_password, signed_in, start
from .diary import choose_date, schedule, homework, new_schedule, diary_marks, about_school, detailed_marks, \
    diary_marks_query, new_marks, information
from ...keyboards.callback import WelcomeCb, WelcomeType, ChooseDateCb, SwitchDiaryCb, DiaryType, MarksCb, MarksType
from ...states.states import Login


def setup(dp: Dispatcher):
    dp.message.register(choose_date, StudentFilter(), F.text == localization.student_main[0], StateFilter('*'))
    dp.message.register(diary_marks, StudentFilter(), ChatType('private'),
                        F.text == localization.student_main[1], StateFilter('*'))
    dp.message.register(about_school, StudentFilter(), ChatType('private'),
                        F.text == localization.student_main[2], StateFilter('*'))
    dp.message.register(new_marks, StudentFilter(), ChatType('private'),
                        F.text == localization.student_main[3], StateFilter('*'))
    dp.message.register(information, StudentFilter(), ChatType('private'),
                        F.text == localization.student_main[4], StateFilter('*'))

    dp.callback_query.register(enter_login, WelcomeCb.filter(F.type == WelcomeType.student), StateFilter('*'))
    dp.message.register(enter_password, GuestFilter(), ChatType('private'), StateFilter(Login.login))
    dp.message.register(signed_in, GuestFilter(), ChatType('private'), StateFilter(Login.password))

    dp.message.register(start, StudentFilter(), ChatType('private'), Command('start'), StateFilter('*'))
    dp.callback_query.register(new_schedule, ChooseDateCb.filter(), StateFilter('*'))
    dp.callback_query.register(schedule, SwitchDiaryCb.filter(F.type == DiaryType.schedule), StateFilter('*'))
    dp.callback_query.register(homework, SwitchDiaryCb.filter(F.type == DiaryType.homework), StateFilter('*'))

    dp.callback_query.register(detailed_marks, MarksCb.filter(F.type == MarksType.detail_marks), StateFilter('*'))
    dp.callback_query.register(diary_marks_query, MarksCb.filter(F.type == MarksType.default_marks), StateFilter('*'))
