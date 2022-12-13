import asyncio

from aiogram.fsm.context import FSMContext
from loguru import logger
from aiogram import exceptions
from aiogram.types import Message

import localization
from tgbot.database import Users
from tgbot.keyboards import default, inline
from tgbot.states.states import Alerts


async def send_message(user_id: int, status, message: Message) -> bool:
    try:
        if status == 'guest':
            await message.send_copy(user_id, reply_markup=inline.welcome.as_markup())
        else:
            await message.send_copy(user_id, reply_markup=default.main.as_markup(resize_keyboard=True))
    except exceptions.TelegramBadRequest:
        logger.error(f"Target [ID:{user_id}]: bad request")
    except exceptions.TelegramRetryAfter as e:
        logger.error(f"Target [ID:{user_id}]: Поймал рейт лимит. Отдыхаю {e.retry_after} секунд.")
        await asyncio.sleep(e.retry_after)
        return await send_message(user_id, status, message)
    except exceptions.TelegramAPIError:
        logger.exception(f"Target [ID:{user_id}]: не удалось отправить")
    else:
        logger.info(f"Target [ID:{user_id}]: успешно отправлено")
        return True
    return False


async def broadcaster(users, message) -> int:
    count = 0
    try:
        for user in users:
            if await send_message(user.user_id, user.status, message):
                count += 1
    finally:
        logger.info(f"{count} сообщений успешно отправлено.")

    return count


async def alert_enter_text(message: Message, state: FSMContext):
    await message.answer(localization.alert_enter_text)
    await state.set_state(Alerts.wait_for_ans)


async def send_alerts(message: Message, state: FSMContext):
    await state.clear()
    users = await Users.filter().all()
    msg = await message.answer(localization.alert_start.format(len(users)))

    count_sent = await broadcaster(users, message)
    await msg.edit_text(localization.alert_end.format(len(users), count_sent))
