from aiogram.filters import BaseFilter
from aiogram.types import Message, Chat


class ChatType(BaseFilter):
    def __init__(self, chat_type: str) -> None:
        self.chat_type = chat_type

    async def __call__(self, message: Message, event_chat: Chat) -> bool:
        return event_chat.type == self.chat_type
