import asyncio
from loguru import logger
import functools

def api_connector(retry_delay: int):
    """ Continiously resends a request if it fails

    Sometimes request could fail. If we do some long living load of data, we dont want to stop this load.
    Resending request usually works well.
    
    As we use lambdas for computations, and if the logic results in infinity loop, lambdas time restrictions
    wont allow us to do this forever. They will stop execution after some amount of time. So we don't care
    of such type os situstions

    Args:
        retry_delay: How long to sleep, if request fails (in seconds)
    """

    def wrapper(func):

        @functools.wraps(func)
        async def wrapped(*args, **kwargs):
            while True:
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    logger.warning('api_request_error', exc_info=e)
                    await asyncio.sleep(retry_delay)

        return wrapped

    return wrapper