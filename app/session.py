import asyncio

from aiohttp_session import Session, get_session, session_middleware
from aiohttp_session.redis_storage import RedisStorage
from redis.asyncio import from_url, RedisError
from structlog import get_logger

from app.exceptions import SessionTimeout

logger = get_logger('respondent-home')


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
