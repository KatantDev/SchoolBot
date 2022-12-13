import datetime
import json

import aiofiles
from aiogram import Bot
from loguru import logger
from tortoise.expressions import Q

import localization
from nschool import NetSchoolAPI
from tgbot.database import Users


async def get_notify(user, bot):
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

    async with aiofiles.open('marks.json', mode='r') as f:
        marks = json.loads(await f.read())

    for days in diary.schedule:
        for lesson in days.lessons:
            for assignment in lesson.assignments:
                if assignment.mark is not None:
                    user_id = str(user.user_id)
                    if user_id not in marks:
                        marks[user_id] = {}
                    if user.login not in marks[user_id]:
                        marks[user_id][user.login] = {}
                    if lesson.subject not in marks[user_id][user.login]:
                        marks[user_id][user.login][lesson.subject] = []
                    date = assignment.deadline
                    mark = [f'{date.day}.{date.month}', assignment.mark]
                    if mark not in marks[user_id][user.login][lesson.subject]:
                        marks[user_id][user.login][lesson.subject].append(mark)
                        if user.notification == 2:
                            await bot.send_message(
                                user.user_id,
                                localization.new_mark.format(
                                    lesson.subject,
                                    assignment.mark,
                                    assignment.content,
                                    assignment.deadline.strftime('%d %B %Y')
                                )
                            )
    async with aiofiles.open('marks.json', mode='w') as f:
        await f.write(json.dumps(marks))
    return marks


async def send_notify(bot: Bot):
    users = await Users.filter(Q(notification=1) | Q(notification=2)).all()
    for user in users:
        try:
            await get_notify(user, bot)
            if user.notification == 1:
                user.notification = 2
                await user.save()
        except Exception as e:
            logger.info(f'Что-то пошло не так... {e}')
