import asyncio
from loguru import logger

from vk_api import VkApi
from vk_api.vk_api import VkApiMethod

loop = asyncio.get_event_loop()

class VKConnection:

    _instance = None
    _token = None
    _conn: VkApi = None

    def __new__(cls):
        if not isinstance(cls._instance, cls):
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    async def create_conn(cls, vk_token: str, api_version: str):
        cls._token = vk_token
        cls._conn = VkApi(token=vk_token, api_version=api_version)
        #cls._conn.auth(token_only=True)
        logger.info(f'new connection to vk')

    def __init__(self):
        pass

    def get_api(self) -> VkApiMethod:
        return self._conn.get_api()
