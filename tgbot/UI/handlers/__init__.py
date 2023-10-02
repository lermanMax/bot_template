from loguru import logger
from aiogram import Dispatcher, Bot, types

from .add_commands import user_commands
from .start import router as start_router
from .help import router as help_router

from .admin import router as admin_router
# from .pars_post import dp

from .utils import router as utils_router

def setup_handlers(dp: Dispatcher):
    dp.include_routers(
        start_router,
        help_router,
        admin_router,
        utils_router,
    )
    logger.info('Handlers configured')


async def setup_commands(bot: Bot):
    # bot.set_chat_menu_button(menu_button=types.MenuButton(type='commands', text='Команды'))
    await bot.set_my_commands(user_commands)
    await bot.set_my_commands(user_commands, scope=types.BotCommandScopeDefault())
    await bot.set_my_commands(user_commands, scope=types.BotCommandScopeAllPrivateChats())
    logger.info('Default commands soccessfully set')