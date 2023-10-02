from __future__ import annotations
from collections import defaultdict
from loguru import logger
from typing import List

from tgbot.loader import scheduler
from tgbot.db_crud.base import AlreadyExist
from tgbot.db_crud.admin_crud import AdminData
from tgbot.db_crud.db_connection import DBConnection
from tgbot.services.tguser import TgUser


class Admin():
    admin_data = AdminData(DBConnection())

    @classmethod
    async def create(cls, tg_id: int,) -> Admin:
        try: 
            await cls.admin_data.create_admin(tg_id)
        except AlreadyExist:
            logger.warning(f"Admin {tg_id} already exist")

    @classmethod
    async def delete(cls, tg_id: int) -> Admin:
        await cls.admin_data.delete_admin(
            admin_id=await cls.admin_data.get_admin_id_by_tg_id(tg_id)
        )
    
    @classmethod
    async def get_all(cls) -> List[Admin]:
        admins_id = await cls.admin_data.get_all_admins_id()
        return [Admin(admin_id) for admin_id in admins_id]

    @classmethod
    async def get_admin_by_tg_id(cls, tg_id: int) -> Admin:
        admin_id = await cls.admin_data.get_admin_id_by_tg_id(tg_id)
        if admin_id:
            return Admin(admin_id)
        else:
            return None

    def __init__(self, admin_id: int):
        self.admin_id = admin_id

    async def get_admin_id(self) -> int:
        return self.admin_id
    
    async def get_tg_id(self) -> int:
        return await self.admin_data.get_tg_id_by_admin_id(self.admin_id)
    
    async def get_tguser(self) -> TgUser:
        tg_id = await self.get_tg_id()
        return await TgUser.get(tg_id)
