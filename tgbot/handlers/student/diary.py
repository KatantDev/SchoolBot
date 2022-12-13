import datetime

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

import localization
from nschool import NetSchoolAPI

from ...keyboards.callback import WelcomeCb, ChooseDateCb, SwitchDiaryCb, MarksCb
from tgbot.database import Users
from tgbot.keyboards import inline


async def get_schedule(user_id, start):
    user = await Users.filter(user_id=user_id).first()
    api = NetSchoolAPI('https://sgo.prim-edu.ru/')
    await api.login(
        user.login,
        user.password,
        'МБОУ \"СОШ № 60\"'
    )
    diary = await api.diary(start=start, end=start)
    await api.logout()

    result = '<b>📅 Расписание:</b>'
    for date in diary.schedule:
        result += f"\n\n<b>🗓 День:</b> <code>{date.day.strftime('%d %B %Y')}</code>\n"
        for lesson in date.lessons:
            result += f"<b>{lesson.start.strftime('%H:%M')} - {lesson.end.strftime('%H:%M')}</b> {lesson.subject}\n"
    return result


async def get_homework(user_id, start):
    user = await Users.filter(user_id=user_id).first()
    api = NetSchoolAPI('https://sgo.prim-edu.ru/')
    await api.login(
        user.login,
        user.password,
        'МБОУ \"СОШ № 60\"'
    )
    diary = await api.diary(start=start, end=start)
    await api.logout()

    result = '<b>📓 Домашнее задание:</b>'
    for date in diary.schedule:
        result += f"\n\n<b>🗓 День:</b> <code>{date.day.strftime('%d %B %Y')}</code>\n"
        for lesson in date.lessons:
            for assignment in lesson.assignments:
                result += f"<b>{lesson.subject}:</b> {assignment.content} "
                if assignment.mark is not None:
                    result += f'(<b>Оценки:</b> {assignment.mark})'
                result += '\n'
    return result


async def get_marks(user_id):
    user = await Users.filter(user_id=user_id).first()
    api = NetSchoolAPI('https://sgo.prim-edu.ru/')
    await api.login(
        user.login,
        user.password,
        'МБОУ \"СОШ № 60\"'
    )

    period = await api.get_period()
    period = period['filterSources'][2]['defaultValue'].split(' - ')
    start = datetime.datetime.strptime(period[0], '%Y-%m-%dT%H:%M:%S.0000000')
    end = datetime.datetime.strptime(period[1], '%Y-%m-%dT%H:%M:%S.0000000')
    diary = await api.diary(start=start, end=end)

    await api.logout()

    marks = {}
    for days in diary.schedule:
        for lesson in days.lessons:
            if lesson.subject not in marks.keys():
                marks[lesson.subject] = []
            for assignment in lesson.assignments:
                if assignment.mark is not None:
                    marks[lesson.subject].append(assignment.mark)
    result = ''
    for lesson in marks.keys():
        if marks[lesson]:
            marks[lesson] = [mark for mark in marks[lesson] if mark]
            general_sum = round(sum(marks[lesson]) / len(marks[lesson]), 1)
            marks[lesson] = ' '.join(str(e) for e in marks[lesson])
            result += f"\n📚<b>{lesson}</b>: {marks[lesson]} | <i>Средний балл:</i> {general_sum}"
    if not result:
        result = localization.no_marks
    return result


async def get_detail_marks(user_id):
    user = await Users.filter(user_id=user_id).first()
    api = NetSchoolAPI('https://sgo.prim-edu.ru/')
    await api.login(
        user.login,
        user.password,
        'МБОУ \"СОШ № 60\"'
    )

    period = await api.get_period()
    period = period['filterSources'][2]['defaultValue'].split(' - ')
    start = datetime.datetime.strptime(period[0], '%Y-%m-%dT%H:%M:%S.0000000')
    end = datetime.datetime.strptime(period[1], '%Y-%m-%dT%H:%M:%S.0000000')
    diary = await api.diary(start=start, end=end)
    await api.logout()
    result = ''
    for days in diary.schedule:
        for lesson in days.lessons:
            for assignment in lesson.assignments:
                if assignment.mark is not None:
                    result += f"\n<b>{assignment.deadline.strftime('%d %B %Y')} 📆 {lesson.subject}:</b> " \
                              f"{assignment.mark} | <i>{assignment.content}</i>"
    if not result:
        result = localization.no_marks
    return result


async def get_school():
    api = NetSchoolAPI('https://sgo.prim-edu.ru/')
    school = await api.school(203)
    return school


async def choose_date(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        '🗓 Выбери дату на которую хочешь узнать расписание.',
        reply_markup=inline.choose_date.as_markup()
    )


def get_date(diary_type, date):
    if date == 'today':
        start = datetime.date.today()
    elif date == 'yesterday':
        start = datetime.date.today() + datetime.timedelta(days=-1)
    elif date == 'tomorrow':
        start = datetime.date.today() + datetime.timedelta(days=1)
    elif date == 'week':
        start = None

    keyboard = inline.switch_diary(diary_type, date)
    return start, keyboard


async def new_schedule(query: CallbackQuery, callback_data: ChooseDateCb):
    date, keyboard = get_date('homework', callback_data.date)
    result = await get_schedule(query.from_user.id, date)
    await query.message.answer(result, reply_markup=keyboard.as_markup())


async def schedule(query: CallbackQuery, callback_data: SwitchDiaryCb):
    date, keyboard = get_date('homework', callback_data.date)
    result = await get_schedule(query.from_user.id, date)
    await query.message.edit_text(result, reply_markup=keyboard.as_markup())


async def homework(query: CallbackQuery, callback_data: SwitchDiaryCb):
    date, keyboard = get_date('schedule', callback_data.date)
    result = await get_homework(query.from_user.id, start=date)
    await query.message.edit_text(result, reply_markup=keyboard.as_markup())


async def diary_marks(message: Message):
    result = await get_marks(message.from_user.id)
    await message.answer(result, reply_markup=inline.detail_marks.as_markup())


async def detailed_marks(query: CallbackQuery):
    result = await get_detail_marks(query.from_user.id)
    await query.message.edit_text(result, reply_markup=inline.marks.as_markup())


async def diary_marks_query(query: CallbackQuery):
    result = await get_marks(query.from_user.id)
    await query.message.edit_text(result, reply_markup=inline.detail_marks.as_markup())


async def about_school(message: Message):
    school = await get_school()
    text = localization.about_school.format(
        school['commonInfo']['schoolName'],
        school['contactInfo']['postAddress'],
        datetime.datetime.strptime(school['commonInfo']['foundingDate'], '%Y-%m-%dT%H:%M:%S').strftime('%d %B %Y'),
        school['contactInfo']['email'],
        school['contactInfo']['web'],
        school['contactInfo']['phones'],
        school['managementInfo']['director'],
        school['managementInfo']['director'],
        school['managementInfo']['principalUVR'],
        school['managementInfo']['principalAHC'],
        school['otherInfo']['inn']
    )
    await message.answer(text)


async def new_marks(message: Message):
    user = await Users.filter(user_id=message.from_user.id).first()
    if user.notification == 0:
        user.notification = 1
        await message.answer(localization.notify_marks_enable)
    elif 1 <= user.notification <= 2:
        user.notification = 0
        await message.answer(localization.notify_marks_disable)
    await user.save()


async def information(message: Message):
    await message.answer(localization.information)
