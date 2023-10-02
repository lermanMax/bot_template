from aiogram import types
from aiogram.filters import Filter
from aiogram.types import Message
from aiogram.types.message import ContentType

from tgbot.loader import bot


class TextButNotComand(Filter):

    async def __call__(self, message: Message) -> bool:
        if message.content_type == ContentType.TEXT:
            if not message.text.startswith('/'):
                return True

        return False