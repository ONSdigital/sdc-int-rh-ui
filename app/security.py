import random
import string
import hashlib

from aiohttp import web
from aiohttp_session import get_session
from aiohttp.web import HTTPForbidden

from . import VALIDATION_FAILURE_MSG
from .flash import flash
from structlog import get_logger

rnd = random.SystemRandom()

logger = get_logger('respondent-home')

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
        "'unsafe-inline'",
        'https://www.googletagmanager.com',
        'https://tagmanager.google.com',
        'https://www.google-analytics.com',
        'https://cdn.ons.gov.uk',
        'https://connect.facebook.net',
    ],
    'connect-src': [
        "'self'",
        'https://www.googletagmanager.com',
        'https://tagmanager.google.com',
        'https://cdn.ons.gov.uk',
    ],
    'img-src': [
        "'self'",
        'data:',
        'https://www.googletagmanager.com',
        'https://cdn.ons.gov.uk',
        'https://www.google-analytics.com',
        'https://www.facebook.com'
    ],
}


FEATURE_POLICY = [
    "layout-animations 'none';",
    "unoptimized-images 'none';",
    "oversized-images 'none';",
    "sync-script 'none';",
    "sync-xhr 'none';",
    "unsized-media 'none';",
]


def _format_csp(csp_dict):
    return ' '.join([
        f"{section} {' '.join(content)};"
        for section, content in csp_dict.items()
    ])


DEFAULT_RESPONSE_HEADERS = {
    'Strict-Transport-Security': 'max-age=31536000 includeSubDomains',
    'Content-Security-Policy': _format_csp(CSP),
    'X-XSS-Protection': '1; mode=block',
    'X-Frame-Options': 'DENY',
    'X-Content-Type-Options': 'nosniff',
    'Referrer-Policy': 'strict-origin-when-cross-origin',
    'Feature-Policy': ' '.join(FEATURE_POLICY),
}

SESSION_KEY = 'identity'


def get_random_string(length):
    allowed_chars = (string.ascii_lowercase + string.ascii_uppercase +
                     string.digits)
    return ''.join(rnd.choice(allowed_chars) for _ in range(length))


async def on_prepare(request: web.BaseRequest, response: web.StreamResponse):
    for header, value in DEFAULT_RESPONSE_HEADERS.items():
        if isinstance(value, str):
            response.headers[header] = value
        else:
            logger.error('Invalid type for header content')


async def check_permission(request):
    """
    Check request permission.
    Raise HTTPForbidden if not previously remembered.
    """
    session = await get_session(request)
    try:
        identity = session[SESSION_KEY]
        logger.info('permission granted',
                    identity=identity,
                    url=request.rel_url.human_repr(),
                    client_ip=request['client_ip'])
    except KeyError:
        flash(request, VALIDATION_FAILURE_MSG)
        logger.warn('permission denied',
                    url=request.rel_url.human_repr(),
                    client_ip=request['client_ip'])
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
                    identity=identity,
                    client_ip=request['client_ip'])
    except KeyError:
        logger.warn('identity not previously remembered',
                    url=request.rel_url.human_repr(),
                    client_ip=request['client_ip'])


async def remember(identity, request):
    """
    Remember identity.
    Modify session with remembered identity.
    """
    session = await get_session(request)
    session[SESSION_KEY] = identity
    logger.info('identity remembered',
                client_ip=request['client_ip'],
                identity=identity)


def get_sha256_hash(uac: str):
    return hashlib.sha256(uac.encode()).hexdigest()
