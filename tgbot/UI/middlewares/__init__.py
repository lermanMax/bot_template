from loguru import logger
from aiogram import Dispatcher

# from .debug_loger import DebugMiddleware
from .authentification import AccessMiddleware, CallbackAccessMiddleware
# from .album import AlbumMiddleware

# if __name__ == "tgbot.middlewares":
#     #dp.middleware.setup(DebugMiddleware())
#     dp.middleware.setup(AlbumMiddleware())
    

def setup_middlewares(dp: Dispatcher):
    dp.message.middleware(AccessMiddleware())
    dp.callback_query.outer_middleware(CallbackAccessMiddleware())
    logger.info('Handlers configured')
