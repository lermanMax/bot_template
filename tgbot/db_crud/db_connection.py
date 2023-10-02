import asyncio
import asyncpg
from loguru import logger


class DBConnection:

    _instance = None
    _cfg = None
    _conn: asyncpg.Connection = None

    def __new__(cls):
        if not isinstance(cls._instance, cls):
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    async def create_conn(cls, cfg, loop):
        cls._cfg = cfg
        cls._conn = await asyncpg.connect(**cfg, loop=loop)

        logger.info(f'new connection to db')
    
    @classmethod
    async def close(cls):
        if cls._conn:
            await cls._conn.close()
    
    # class decorator. when method excepted, it will be called again after 1 second.
    @staticmethod
    def retry(func):
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except asyncpg.exceptions.InterfaceError as e:
                logger.error(e)
                await asyncio.sleep(0.5)
                return await wrapper(*args, **kwargs)
        return wrapper

    def __init__(self):
        pass
    
    @retry
    async def execute(self, query: str, *args):
        return await self._conn.execute(query, *args)

    @retry
    async def fetchval(self, query, *args):
        return await self._conn.fetchval(query, *args)

    @retry
    async def fetch(self, query, *args):
        return await self._conn.fetch(query, *args)
