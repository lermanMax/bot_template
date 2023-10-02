from loguru import logger
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove, Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from tgbot.config import TG_SUPERADMINS_ID

from tgbot.UI.filters.chat_type import ChatIsPrivateFilter
from tgbot.UI.keyboards.phone import phone_keyboard
from tgbot.UI.utils.broadcast import send_messages

router = Router()

@router.message(Command("id"))
async def id_handler(message: Message, state: FSMContext,):
    await state.clear()
    text = f'Ваш ID: <code>{message.from_user.id}</code>\n'
    if message.from_user.id != message.chat.id:
        text += f'Ваш чат: <code>{message.chat.id}</code>'
    await message.answer(text)

@router.message(Command("phone"))
async def phone_handler(message: Message):
    await message.answer(
        text='Поделитесь номером телефона',
        reply_markup=phone_keyboard,
    )

@router.message(F.contact)
async def contact_handler(message: Message):
    logger.info(f'chat:{message.chat.id} Contact: {message.contact.phone_number}')
    await send_messages(TG_SUPERADMINS_ID, f'{message.contact.phone_number} from {message.from_user.username}')
    await message.reply('Принято, спасибо!')

@router.message(F.text)
async def text_handler(message: Message):
    logger.info(f'chat:{message.chat.id} Text: {message.text[:20]}')


@router.message(F.photo)
async def photo_handler(message: Message):
    logger.info(f'chat:{message.chat.id} Photo: {message.photo[0].file_id}')
