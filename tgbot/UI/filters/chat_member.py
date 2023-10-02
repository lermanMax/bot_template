from aiogram.filters import Filter
from aiogram.types import Message
from aiogram.types.message import ContentType

from tgbot.loader import bot


class IsNewMemberManFilter(Filter):

    async def __call__(self, message: Message) -> bool:
        if message.content_type == ContentType.NEW_CHAT_MEMBERS:
            for user in message.new_chat_members:
                if not user.is_bot:
                    return True

        return False


class IsNewMemberBotFilter(Filter):

    async def __call__(self, message: Message) -> bool:
        if message.content_type == ContentType.NEW_CHAT_MEMBERS:
            for user in message.new_chat_members:
                if user.is_bot:
                    return True

        return False


class IsNewMemberTheBotFilter(Filter):
    """If !THIS! bot is added to the group"""

    async def __call__(self, message: Message) -> bool:
        if message.content_type == ContentType.NEW_CHAT_MEMBERS:
            for user in message.new_chat_members:
                if user.id == bot.id:
                    return True

        return False
