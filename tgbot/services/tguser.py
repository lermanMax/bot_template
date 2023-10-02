from __future__ import annotations
from collections import defaultdict
from loguru import logger
from typing import List

from tgbot.loader import scheduler
from tgbot.services.base import CacheMixin
from tgbot.db_crud.base import AlreadyExist
from tgbot.db_crud.tguser_crud import TgUserData
from tgbot.db_crud.db_connection import DBConnection


class TgUser(CacheMixin):
    save_in_cache: bool = True
    tg_data: TgUserData = TgUserData(DBConnection())

    @classmethod
    async def create(
        cls, tg_id: int,
        first_name: str,
        last_name: str, 
        tg_username: str,
    ) -> None:
        try:
            await cls.tg_data.create_tg_user(tg_id, first_name, last_name, tg_username)
        except AlreadyExist:
            logger.warning(f"tg_user {tg_id} already exist")
    
    @classmethod
    async def get_all(cls) -> List[TgUser]:
        tgusers_id = await cls.tg_data.get_all_tg_users()
        return [await TgUser.get(tg_id) for tg_id in tgusers_id]

    @classmethod
    async def _get(cls, tg_id: int) -> TgUser:
        """init method"""
        if not await cls.tg_data.check_tg_user_exists(tg_id):
            return None
        self = cls()
        super(TgUser, self).__init__(key=tg_id) 
        self.tg_id = tg_id
        return self

    def __init__(self):
        pass

    async def get_tg_id(self) -> int:
        return self.tg_id

    async def get_username(self) -> str:
        username = await self.tg_data.get_tg_username(self.tg_id)
        if not username:
            return self.tg_id
        else:
            return username
    
    async def get_first_name(self) -> str:
            return await self.tg_data.get_first_name(self.tg_id)
    
    async def get_last_name(self) -> str:
        return await self.tg_data.get_last_name(self.tg_id)
    
    async def get_full_name(self) -> str:
        return f'{await self.get_first_name()} {await self.get_last_name()}'

    async def is_blocked(self) -> bool:
        return await self.tg_data.is_blocked(self.tg_id)

    async def ban(self):
        logger.info(f'ban: {self.tg_id}')
        await self.tg_data.block(self.tg_id)

    async def unban(self):
        logger.info(f'unban: {self.tg_id}')
        await self.tg_data.unblock(self.tg_id)
