from aiogram import Dispatcher, F
from aiogram.filters import Command, StateFilter

from .welcome import start, start_query
from .guest import guest, continue_info
from tgbot.filters.chat_type import ChatType
from tgbot.filters.role import GuestFilter
from ...keyboards.callback import WelcomeCb, WelcomeType
from ...states.states import Feedback, Login


def setup(dp: Dispatcher):
    dp.message.register(start, GuestFilter(), ChatType('private'), Command('start'))
    dp.callback_query.register(start_query, WelcomeCb.filter(F.type == WelcomeType.return_main),
                               StateFilter('*'))
    dp.callback_query.register(guest, WelcomeCb.filter(F.type == WelcomeType.not_student), StateFilter('*'))
    dp.message.register(continue_info, GuestFilter(), ChatType('private'), StateFilter(Feedback.wait_for_ans))
