import os
import subprocess
import asyncio
from loguru import logger

from aiogram import Dispatcher, Bot

from tgbot.loader import bot, scheduler
from tgbot.config import TG_SUPERADMINS_ID
from tgbot.db_crud.db_connection import DBConnection
from tgbot.config import DB_HOST, DB_NAME, DB_USER, DB_PASS, DB_PORT

from tgbot.UI.handlers import setup_handlers, setup_commands
from tgbot.UI.middlewares import setup_middlewares
from tgbot.UI.utils.broadcast import send_messages


def get_git_version() -> str:
    try:
        version = subprocess.check_output(["git", "describe"]).strip()
    except:
        version = '0'
    return version

async def connect_db(dp: Dispatcher):
    dp.db_connection = DBConnection()
    db_config = {
        'host': DB_HOST,
        'database': DB_NAME,
        'user': DB_USER,
        'password': DB_PASS,
        'port': DB_PORT}
    await dp.db_connection.create_conn(
        cfg = db_config,
        loop = asyncio.get_event_loop()
    )

async def on_shutdown(dp: Dispatcher):
    logger.info('Shutdown')

    scheduler.shutdown()
    logger.info('scheduler shutdown')

    await dp.db_connection.close()
    logger.info('DB connection closed')


async def main():
    logger.info('Starting on polling mode ...')
    logger.info(f'Version: {get_git_version()}')
    dp = Dispatcher()

    await setup_commands(bot)

    await connect_db(dp)
    setup_handlers(dp)
    setup_middlewares(dp)

    logger.info("started")
    await send_messages(TG_SUPERADMINS_ID, 'started')
    try:
        await dp.start_polling(bot)
    finally:
        logger.info("stopped")
        await on_shutdown(dp)
        await send_messages(TG_SUPERADMINS_ID,'stopped')


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())