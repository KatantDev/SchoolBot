import asyncio

from aiogram.fsm.context import FSMContext
from aiogram.methods import SendChatAction, SendMessage
from aiogram.types import CallbackQuery, Message
from localization import not_student, feedback, welcome
from tgbot import config
from tgbot.keyboards import inline
from tgbot.states.states import Feedback


async def guest(query: CallbackQuery, state: FSMContext):
    await query.message.delete_reply_markup()
    await SendChatAction(chat_id=query.from_user.id, action='typing')
    await asyncio.sleep(1)
    await query.message.answer(not_student[0])
    await SendChatAction(chat_id=query.from_user.id, action='typing')
    await asyncio.sleep(2)
    await query.message.answer(not_student[1], reply_markup=inline.school_link.as_markup())
    await SendChatAction(chat_id=query.from_user.id, action='typing')
    await asyncio.sleep(6)
    await query.message.answer(not_student[2], reply_markup=inline.inst_link.as_markup())
    await SendChatAction(chat_id=query.from_user.id, action='typing')
    await asyncio.sleep(6)
    await query.message.answer(not_student[3], reply_markup=inline.return_main.as_markup())
    await state.set_state(Feedback.wait_for_ans)


async def continue_info(message: Message, state: FSMContext):
    await state.clear()
    await SendMessage(
        chat_id=config.LOG_CHAT,
        text=feedback.format(message.from_user.id, message.from_user.full_name, message.text)
    )
    await SendChatAction(chat_id=message.from_user.id, action='typing')
    await asyncio.sleep(1)
    await message.answer(not_student[4], reply_markup=inline.dnevnik_link.as_markup())
    await asyncio.sleep(6)
    await message.answer(not_student[5])
    await asyncio.sleep(3)
    await message.answer(not_student[6])
    await asyncio.sleep(4)
    await message.answer(welcome['start'], reply_markup=inline.welcome.as_markup())
