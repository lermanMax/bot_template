from typing import Union

from aiogram.filters import Filter
from aiogram.types import Message


class ChatIsGroupFilter(Filter):

    async def __call__(self, message: Message) -> bool:
        return message.chat.type in ["group", "supergroup"]


class ChatIsPrivateFilter(Filter):

    async def __call__(self, message: Message) -> bool:
        return message.chat.type in ["private"]
