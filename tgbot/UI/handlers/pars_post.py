from typing import List
from loguru import logger
import asyncio
from aiogram.dispatcher.filters import CommandStart, ChatTypeFilter, CommandHelp
from aiogram.types import Message, ReplyKeyboardRemove, ChatType, Message, CallbackQuery, ContentType
from aiogram.dispatcher import FSMContext

from tgbot.loader import dp, bot
from tgbot.config import TG_CHANNEL, TG_CHANNEL_FOR_DONORS, VK_OWNER_ID
from tgbot.filters.from_where import IsNewPostInChannelFilter
from tgbot.services.post_reposter import Reposter
from tgbot.utils.pars_messages import parse_message, Post


@dp.channel_post_handler(IsNewPostInChannelFilter())
async def got_post(message: Message,):
    await new_post_handler(message)

@dp.channel_post_handler(IsNewPostInChannelFilter(), is_media_group=True, content_types=ContentType.ANY)
async def got_album_post(message: Message, album: List[Message]):
    logger.info(f'New album of {len(album)} posts from {message.chat.id}: ')
    await new_post_handler(message, album=album)

@dp.channel_post_handler(IsNewPostInChannelFilter(), content_types=ContentType.PHOTO)
async def got_photo_post(message: Message,):
    logger.info(f'New photo post from {message.chat.id}')
    await new_post_handler(message)

@dp.channel_post_handler(IsNewPostInChannelFilter(), content_types=ContentType.VIDEO)
async def got_video_post(message: Message,):
    logger.info(f'New video post from {message.chat.id}')
    await new_post_handler(message)

@dp.channel_post_handler(IsNewPostInChannelFilter(), content_types=ContentType.DOCUMENT)
async def got_document_post(message: Message,):
    logger.info(f'New document post from {message.chat.id}')
    await new_post_handler(message)

@dp.channel_post_handler(IsNewPostInChannelFilter(), content_types=ContentType.POLL)
async def got_poll_post(message: Message,):
    logger.info(f'New poll post from {message.chat.id}')
    await new_post_handler(message)


async def new_post_handler(message: Message, album: List[Message] = None):
    await asyncio.sleep(3)
    if await Reposter().is_post_reposted(chanal_id=message.chat.id, tg_id=message.message_id):
        logger.info(f'Post is reposted {message.chat.id} {message.message_id}.')
        return

    logger.info(f'New post from {message.chat.id} {message.message_id}.')

    if (str(message.chat.id) == TG_CHANNEL_FOR_DONORS) or (message.chat.mention == TG_CHANNEL_FOR_DONORS):
        for_donut = True
    else:
        for_donut = False

    post: Post = await parse_message(message, album=album)
    await Reposter().add_post(
        post=post,
        vk_owner_id=VK_OWNER_ID,
        tg_chat_id=message.chat.id,
        tg_id=message.message_id,
        for_donut=for_donut
    )
