from loguru import logger
from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery

from tgbot.services.tguser import TgUser


async def _get_tguser(tg_id: int):
        tguser = await TgUser.get(tg_id)
        if tguser:
            if await tguser.is_blocked():
                logger.warning(f'Пользователь {tg_id} заблокирован!')
                return None

        return tguser


class AccessMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        logger.info(f'event from: {event.from_user.id}')
        tg_id = event.from_user.id
        tguser = await _get_tguser(tg_id)
        if tguser or event.text.startswith('/start'):
            data['tguser'] = tguser
            return await handler(event, data)
        
        return await event.answer('Access faild')


class CallbackAccessMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
        event: CallbackQuery,
        data: Dict[str, Any]
    ) -> Any:
        logger.info(f'callback event from: {event.from_user.id}')
        tg_id = event.from_user.id
        tguser = await _get_tguser(tg_id)
        if tguser:
            data['tguser'] = tguser
            return await handler(event, data)
        
        return
