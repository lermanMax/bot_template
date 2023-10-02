from loguru import logger
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove, Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from tgbot.loader import bot
from tgbot.services.tguser import TgUser, AlreadyExist
from tgbot.config import TGBOT_USERNAME, TG_SUPERADMINS_ID

from tgbot.UI.filters.chat_type import ChatIsPrivateFilter


router = Router()

@router.message(Command("start"), ChatIsPrivateFilter(),)
async def start_menu_handler(message: Message, tguser: TgUser):
    if not isinstance(tguser, TgUser):
        await TgUser.create(
            tg_id=message.from_user.id,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
            tg_username=message.from_user.username,
        )
        tguser: TgUser = await TgUser.get(message.from_user.id)

    text = f'Hello, {await tguser.get_first_name()}'
    await message.answer(text)
