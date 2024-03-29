import hashlib
import random
import string

from aiohttp import web
from aiohttp.web import HTTPForbidden
from aiohttp_session import Session, get_session
from structlog import get_logger

from app.session import get_existing_session

CSP = {
    'default-src': [
        "'self'",
        'https://cdn.ons.gov.uk',
    ],
    'font-src': [
        "'self'",
        'data:',
        'https://cdn.ons.gov.uk',
    ],
    'script-src': [
        "'self'",
        'https://cdn.ons.gov.uk',
    ],
    'connect-src': [
        "'self'",
        'https://cdn.ons.gov.uk',
    ],
    'img-src': [
        "'self'",
        'data:',
        'https://cdn.ons.gov.uk'
    ],

}

DEFAULT_RESPONSE_HEADERS = {
    'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
    'Content-Security-Policy': CSP,
    'X-Content-Security-Policy': CSP,
    'X-Frame-Options': 'DENY',
    'X-Content-Type-Options': 'nosniff',
    'Referrer-Policy': 'strict-origin-when-cross-origin',
    'X-Permitted-Cross-Domain-Policies': 'None',
    'clear-site-data': '"storage"',
    'Cross-Origin-Opener-Policy': 'same-origin',
    'Cross-Origin-Resource-Policy': 'same-site',
    'Cache-Control': ['no-store', 'max-age=0'],
    'Server': 'Office For National Statistics',
    'Permissions-Policy': 'accelerometer=(),autoplay=(),camera=(),display-capture=(),document-domain=(),'
                          'encrypted-media=(),fullscreen=(),geolocation=(),gyroscope=(),magnetometer=(),microphone=('
                          '),midi=(),payment=(),picture-in-picture=(),publickey-credentials-get=(),screen-wake-lock=('
                          '),sync-xhr=(self),usb=(),xr-spatial-tracking=()'
}

ADD_NONCE_SECTIONS = [
    'script-src',
]

ADD_AIMS_URL_SECTIONS = [
    'connect-src',
]

SESSION_KEY = 'identity'

rnd = random.SystemRandom()

logger = get_logger('respondent-home')


def get_random_string(length):
    allowed_chars = (string.ascii_lowercase + string.ascii_uppercase +
                     string.digits)
    return ''.join(rnd.choice(allowed_chars) for _ in range(length))


@web.middleware
async def nonce_middleware(request, handler):
    request.csp_nonce = get_random_string(16)
    return await handler(request)


async def on_prepare(request: web.BaseRequest, response: web.StreamResponse):
    for header, value in DEFAULT_RESPONSE_HEADERS.items():
        if isinstance(value, dict):
            value = '; '.join([
                f"{section} {' '.join(content)} 'nonce-{request.csp_nonce}'"
                if section in ADD_NONCE_SECTIONS else
                f"{section} {' '.join(content)}"
                for section, content in value.items()
            ])
        elif not isinstance(value, str):
            value = ' '.join(value)
        response.headers[header] = value


async def context_processor(request):
    return {
        'cspNonce': request.csp_nonce,
    }


async def get_permitted_session(request) -> Session:
    """
    Check request permission.
    Raise HTTPForbidden if existing session and not previously remembered, else return session.
    """
    session = await get_existing_session(request, 'start')
    try:
        identity = session[SESSION_KEY]
        logger.info('permission granted',
                    client_ip=request['client_ip'],
                    client_id=request['client_id'],
                    trace=request['trace'],
                    identity=identity,
                    url=request.rel_url.human_repr())
        return session
    except KeyError:
        logger.warn('permission denied',
                    client_ip=request['client_ip'],
                    client_id=request['client_id'],
                    trace=request['trace'],
                    url=request.rel_url.human_repr())
        raise HTTPForbidden


async def forget(request):
    """
    Forget identity.
    Modify session to remove previously remembered identity.
    """
    session = await get_session(request)
    try:
        identity = session[SESSION_KEY]
        session.pop(SESSION_KEY, None)
        logger.info('identity forgotten',
                    client_ip=request['client_ip'],
                    client_id=request['client_id'],
                    trace=request['trace'],
                    identity=identity)
    except KeyError:
        logger.warn('identity not previously remembered',
                    client_ip=request['client_ip'],
                    client_id=request['client_id'],
                    trace=request['trace'],
                    url=request.rel_url.human_repr())


async def remember(identity, request):
    """
    Remember identity.
    Modify session with remembered identity.
    """
    session = await get_session(request)
    session[SESSION_KEY] = identity
    logger.info('identity remembered',
                client_ip=request['client_ip'],
                client_id=request['client_id'],
                trace=request['trace'],
                identity=identity)


async def invalidate(request):
    """
    Invalidate open session.
    """
    session = await get_session(request)
    try:
        session.invalidate()
        logger.info('session invalidated',
                    client_ip=request['client_ip'],
                    client_id=request['client_id'],
                    trace=request['trace'])
    except KeyError:
        logger.warn('session already invalidated',
                    client_ip=request['client_ip'],
                    client_id=request['client_id'],
                    trace=request['trace'])


def get_sha256_hash(uac: str):
    return hashlib.sha256(uac.encode()).hexdigest()
