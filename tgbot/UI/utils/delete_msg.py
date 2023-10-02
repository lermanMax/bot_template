from loguru import logger

from aiogram.types import Message
from aiogram import exceptions
from datetime import datetime

from tgbot.loader import bot, scheduler
from tgbot.config import TGBOT_USERNAME


async def delete_message_at_time(message: Message, date_time: datetime) -> None:

    async def delete_message() -> None:
        try:
            await message.delete()
            logger.info('Message was deleted')
        except exceptions.AiogramError:
            logger.info('Message was not modified')
    
    scheduler.add_job(delete_message, 'date', run_date=date_time)
    logger.info(f'Message will delete at {date_time}')
