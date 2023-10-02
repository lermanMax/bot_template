from loguru import logger

from tgbot.loader import dp, bot, scheduler
from tgbot.config import TGBOT_USERNAME, INTERVAL



async def create_schedule_for_checking_triggers() -> None:

    async def check_all_notifications() -> None:
        logger.info('start check')
        
        logger.info('end check')
    
    # add job to sheduler
    scheduler.add_job(
        check_all_notifications,
        'interval',
        seconds=INTERVAL,
    )

    logger.info(f'Schedule started. Interval {INTERVAL}sec.')

