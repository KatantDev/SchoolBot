from aiogram.filters.state import State, StatesGroup


class Feedback(StatesGroup):
    wait_for_ans = State()


class Login(StatesGroup):
    login = State()
    password = State()


class Alerts(StatesGroup):
    wait_for_ans = State()