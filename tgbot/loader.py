from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pytz import timezone

from tgbot.config import TGBOT_TOKEN

# Setup bot
bot = Bot(token=TGBOT_TOKEN, parse_mode="HTML")

# timezone
tz = timezone('Europe/Moscow')

# Setup scheduler
scheduler = AsyncIOScheduler(timezone=tz)
scheduler.start()
