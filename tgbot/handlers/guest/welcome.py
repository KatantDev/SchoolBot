from loguru import logger
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from localization import welcome
from tgbot.database import Users
from tgbot.keyboards import inline


async def start(message: Message):
    user = await Users.filter(user_id=message.from_user.id).first()
    if user is None:
        await Users.create(
            user_id=message.from_user.id,
            status='guest',
            notification=0
        )
        logger.info(f'New user added in database | USER ID: {message.from_user.id}')
    await message.answer(welcome['start'], reply_markup=inline.welcome.as_markup())


async def start_query(query: CallbackQuery, state: FSMContext):
    await state.clear()
    await query.message.edit_text(welcome['start'], reply_markup=inline.welcome.as_markup())
