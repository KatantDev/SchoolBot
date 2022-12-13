from aiogram import Dispatcher
from aiogram.filters import Command, StateFilter

from tgbot.filters.role import AdminFilter
from .alerts import alert_enter_text, send_alerts
from ...states.states import Alerts


def setup(dp: Dispatcher):
    dp.message.register(alert_enter_text, AdminFilter(), Command('alert'))
    dp.message.register(send_alerts, AdminFilter(), StateFilter(Alerts.wait_for_ans))
