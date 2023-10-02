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

@router.message(Command("help"), ChatIsPrivateFilter(),)
async def help_menu_handler(message: Message, state: FSMContext,):
    logger.info(f'help_menu_handler: {message.from_user.id}')
    await state.clear()
    text = (
        f'Список команд:\n'
        f'/start - начать\n'
        f'/help - помощь\n'
        f'\n'
        f'Если у вас есть вопросы или проблемы, напишите разработчику: @LermanMax'
    )
    await message.answer(text)
