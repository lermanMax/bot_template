from loguru import logger
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove, Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from tgbot.loader import bot
from tgbot.services.tguser import TgUser
from tgbot.services.admin import Admin

from tgbot.UI.filters.admin import IsUserAdminFilter
from tgbot.UI.filters.chat_member import IsNewMemberTheBotFilter, IsNewMemberBotFilter
from tgbot.UI.keyboards.inline import make_inline_keyboard, SimpleCbFactory


router = Router()

@router.message(Command("admin"), IsUserAdminFilter(),)
async def get_admin_menu(message: Message, tguser: TgUser, state: FSMContext,):
    logger.info(f'tguser: {await tguser.get_tg_id()}')
    text = 'Вы открыли меню, доступное только администраторам:'
    keyboard = await make_inline_keyboard(
        question_name='admin_menu',
        answers=[
            'Посмотреть всех юзеров',
            'Все администраторы',
        ]
    )
    await state.clear()
    await message.answer(text, reply_markup=keyboard)


@router.callback_query(SimpleCbFactory.filter(F.question == 'admin_menu'))
async def admin_menu_push(
        callback: CallbackQuery, 
        callback_data: SimpleCbFactory
):
    await callback.answer()
    await answers_methods[callback_data.answer](message=callback.message)

async def get_all_users(message: Message):
    text = f'Все Юзеры:\n'
    for tguser in await TgUser.get_all():
        text += f'<a href="tg://user?id={tguser.tg_id}">{await tguser.get_full_name()}</a>'
    await message.answer(text)

async def get_all_admins(message: Message):
    text = f'Все Администраторы:\n'
    for admin in await Admin.get_all():
        tguser = await admin.get_tguser()
        text += f'<a href="tg://user?id={tguser.tg_id}">{await tguser.get_full_name()}</a>'
    await message.answer(text)

answers_methods = {
    'Посмотреть всех юзеров': get_all_users,
    'Все администраторы': get_all_admins,
}