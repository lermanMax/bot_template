from aiogram import types
from aiogram.filters import Filter
from aiogram.types import Message
from aiogram.types.message import ContentType

from tgbot.loader import bot
from tgbot.config import TG_COMMENTS, TG_CHANNEL


class IsNewCommentPostFilter(Filter):

    async def __call__(self, message: Message) -> bool:
        if message.content_type == ContentType.TEXT:
            if message.chat.id in (TG_COMMENTS, ):
                return True
        return False


class IsNewPostInChannelFilter(Filter):

    async def __call__(self, message: Message) -> bool:
        if (str(message.chat.id) in (TG_CHANNEL, )
                or message.chat.mention in (TG_CHANNEL, )):
            return True
        else:
            return False
