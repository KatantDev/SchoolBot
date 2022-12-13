from aiogram.filters.callback_data import CallbackData
from enum import Enum


class WelcomeType(str, Enum):
    student = 'student'
    not_student = 'not_student'
    return_main = 'return_main'


class DiaryType(str, Enum):
    homework = 'homework'
    schedule = 'schedule'


class MarksType(str, Enum):
    default_marks = 'marks'
    detail_marks = 'detail_marks'


class WelcomeCb(CallbackData, prefix='welcome'):
    type: WelcomeType


class ChooseDateCb(CallbackData, prefix='choose_date'):
    date: str


class SwitchDiaryCb(CallbackData, prefix='switch_diary'):
    type: DiaryType
    date: str


class MarksCb(CallbackData, prefix='marks'):
    type: MarksType
