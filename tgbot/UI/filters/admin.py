from aiogram.types import Message
from aiogram.filters import Filter

from tgbot.services.admin import Admin
from tgbot.config import TG_SUPERADMINS_ID


class IsUserSuperadminFilter(Filter):

    async def __call__(self, message: Message) -> bool:
        return bool(message.from_user.id in TG_SUPERADMINS_ID)


class IsUserAdminFilter(Filter):

    async def __call__(self, message: Message) -> bool:
        admin = await Admin.get_admin_by_tg_id(message.from_user.id)
        return isinstance(admin, Admin)
