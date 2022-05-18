import asyncio
import time

from aiohttp_session import session_middleware, Session, get_session
from aiohttp_session.redis_storage import RedisStorage
from aioredis import from_url, RedisError
from structlog import get_logger

from .exceptions import SessionTimeout

logger = get_logger('respondent-home')

# Please see https://github.com/aio-libs/aiohttp-session/issues/344
# Anomalous behaviour can arise where you have a valid session cookie from the client as if a session was created by
# a previous request but cannot retrieve the session data in Redis, although the data will be in Redis. This behaviour
# was introduced with Pull Request: https://github.com/aio-libs/aiohttp-session/pull/331
# Monkey patch aiohttp_session Session.__init__ method to remove suspect behaviour.


def setup(app_config):
    loop = asyncio.get_event_loop()
    redis_pool = loop.run_until_complete(
        make_redis_pool(app_config['REDIS_SERVER'], app_config['REDIS_PORT']))
    return session_middleware(
        RedisStorage(redis_pool,
                     cookie_name='RH_SESSION',
                     max_age=int(app_config['SESSION_AGE'])))


async def make_redis_pool(host, port):
    redis_host = "redis://" + host + ":" + port
    try:
        redis = from_url(
            redis_host
        )
        return redis
    except (OSError, RedisError):
        logger.error('failed to create redis connection')


async def get_existing_session(request, user_journey, request_type=None) -> Session:
    session = await get_session(request)
    if not session.new:
        return session
    else:
        logger.warn('session timed out',
                    client_ip=request['client_ip'],
                    client_id=request['client_id'],
                    trace=request['trace'])
        raise SessionTimeout(user_journey, request_type)


def get_session_value(request, session, key, user_journey, request_type=None):
    try:
        return session[key]
    except KeyError:
        logger.info(f'Failed to extract session key {key}',
                    client_ip=request['client_ip'],
                    client_id=request['client_id'],
                    trace=request['trace'])
        raise SessionTimeout(user_journey, request_type)
