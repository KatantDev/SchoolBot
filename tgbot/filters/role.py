from aiogram.filters import BaseFilter
from aiogram.types import Message
from ..database import Users


class GuestFilter(BaseFilter):
    guest: str = 'guest'

    async def __call__(self, message: Message) -> bool:
        user = await Users.filter(user_id=message.from_user.id).first()
        if user is None:
            return True
        else:
            return user.status == self.guest


class StudentFilter(BaseFilter):
    student: list = ['student', 'admin']

    async def __call__(self, message: Message) -> bool:
        user = await Users.filter(user_id=message.from_user.id).first()
        if user is None:
            return False
        else:
            return user.status in self.student


class AdminFilter(BaseFilter):
    admin: str = 'admin'

    async def __call__(self, message: Message) -> bool:
        user = await Users.filter(user_id=message.from_user.id).first()
        if user is None:
            return False
        else:
            return user.status == self.admin
