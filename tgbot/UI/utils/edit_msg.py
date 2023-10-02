from loguru import logger
from aiogram.types import Message, InlineKeyboardMarkup
from aiogram.exceptions import AiogramError

from tgbot.services.tguser import TgUser
from tgbot.loader import bot


async def try_edit_reply_markup(message:Message, reply_markup: InlineKeyboardMarkup):
    try:
        await message.edit_reply_markup(reply_markup)
    except AiogramError as e:
        logger.error(e)
        logger.error(f'Message not edited {message.text[:15]}...')
    except Exception as e:
        logger.error(e)
        

async def unpin_all_messages_for_all_tgusers():
    for tguser in await TgUser.get_all():
        tguser: TgUser
        try:
            await bot.unpin_all_chat_messages(await tguser.get_tg_id())
        except AiogramError as e:
            logger.error(e)
        except Exception as e:
            logger.error(e)
        # except ChatNotFound:
        #     logger.warning(f'ChatNotFound {tguser.get_tg_id()}...')
        # except BotBlocked:
        #     logger.warning(f'BotBlocked {tguser.get_tg_id()}...')
