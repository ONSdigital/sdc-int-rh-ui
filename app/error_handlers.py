import aiohttp_jinja2 as jinja

from aiohttp import web
from aiohttp.client_exceptions import (ClientResponseError,
                                       ClientConnectorError,
                                       ClientConnectionError, ContentTypeError)
from aiohttp.web_exceptions import HTTPServerError
from aioredis import RedisError

from .exceptions import (InactiveUacError, AlreadyReceiptedUacError,
                         InvalidForEqTokenGeneration, InvalidAccessCode,
                         SessionTimeout, TooManyRequestsEQLaunch)
from structlog import get_logger

from .utils import View

from . import (START_PAGE_TITLE_EN, START_PAGE_TITLE_CY)

from .security import invalidate

logger = get_logger('respondent-home')


def create_error_middleware(overrides):
    @web.middleware
    async def middleware_handler(request, handler):
        try:
            resp = await handler(request)
            override = overrides.get(resp.status)
            return await override(request) if override else resp
        except web.HTTPNotFound:
            path_prefix = request.app['URL_PATH_PREFIX']

            def path_starts_with(suffix):
                return request.path.startswith(path_prefix + suffix)

            index_resource = request.app.router['Start:get']

            if path_starts_with('/cy'):
                display_region = 'cy'
            else:
                display_region = 'en'

            if request.path + '/' == index_resource.canonical.replace('{display_region}', display_region):
                logger.debug('redirecting to index',
                             client_ip=request['client_ip'],
                             client_id=request['client_id'],
                             trace=request['trace'],
                             path=request.path)
                raise web.HTTPMovedPermanently(index_resource.url_for(display_region=display_region))
            return await not_found_error(request)
        except web.HTTPForbidden:
            return await forbidden(request)
        except InvalidAccessCode:
            return await invalid_access_code(request)
        except SessionTimeout as ex:
            return await session_timeout(request, ex.user_journey, ex.request_type)
        except TooManyRequestsEQLaunch:
            return await too_many_requests_eq_launch(request)
        except AlreadyReceiptedUacError:
            return await receipted_uac(request)
        except InactiveUacError:
            return await uac_inactive(request)
        except InvalidForEqTokenGeneration as ex:
            return await eq_error(request, ex.message)
        except ClientConnectionError as ex:
            return await connection_error(request, ex.args[0])
        except ClientConnectorError as ex:
            return await connection_error(request, ex.os_error.strerror)
        except ContentTypeError as ex:
            return await payload_error(request, str(ex.request_info.url))
        except KeyError as error:
            return await key_error(request, error)
        except ClientResponseError as ex:
            return await response_error(request, ex)
        except RedisError as ex:
            return await internal_error('Redis connection error', request, ex)
        except HTTPServerError as ex:
            return await internal_error('An unknown server error has occurred', request, ex)

    return middleware_handler


async def receipted_uac(request):
    logger.warn('attempt to use a receipted access code',
                client_ip=request['client_ip'],
                client_id=request['client_id'],
                trace=request['trace'])
    attributes = check_display_region(request)
    return jinja.render_template('start-uac-already-used.html', request, attributes)


async def uac_inactive(request):
    logger.warn('attempt to use an uac thats marked inative',
                client_ip=request['client_ip'],
                client_id=request['client_id'],
                trace=request['trace'])
    attributes = check_display_region(request)
    return jinja.render_template('start-uac-inactive.html', request, attributes)


async def eq_error(request, message: str):
    logger.error('service failed to get EQ token',
                 client_ip=request['client_ip'],
                 client_id=request['client_id'],
                 trace=request['trace'],
                 exception=message)
    attributes = check_display_region(request)
    return jinja.render_template('error.html', request, attributes, status=500)


async def connection_error(request, message: str):
    logger.error('service connection error',
                 client_ip=request['client_ip'],
                 client_id=request['client_id'],
                 trace=request['trace'],
                 exception=message)
    attributes = check_display_region(request)
    return jinja.render_template('error.html', request, attributes, status=500)


async def payload_error(request, url: str):
    logger.error('service failed to return expected json payload',
                 client_ip=request['client_ip'],
                 client_id=request['client_id'],
                 trace=request['trace'],
                 url=url)
    attributes = check_display_region(request)
    return jinja.render_template('error.html', request, attributes, status=500)


async def key_error(request, error):
    logger.error('required value ' + str(error) + ' missing',
                 client_ip=request['client_ip'],
                 client_id=request['client_id'],
                 trace=request['trace'],
                 missing_key=error)
    attributes = check_display_region(request)
    return jinja.render_template('error.html', request, attributes, status=500)


async def response_error(request, ex: ClientResponseError = None):
    tracking = {"client_ip": request['client_ip'], "client_id": request['client_id'], "trace": request['trace']}
    if ex:
        logger.error('response error',
                     **tracking,
                     url=str(ex.request_info.url),
                     method=ex.request_info.method,
                     status=ex.status,
                     exception=ex.message)
    else:
        logger.error('uncaught response error', **tracking)

    attributes = check_display_region(request)
    return jinja.render_template('error.html', request, attributes, status=500)


async def internal_error(message, request, ex):
    logger.error(message,
                 exception=ex)
    attributes = check_display_region(request)
    _get_site_name(attributes, request)
    return jinja.render_template('error.html', request, attributes, status=500)


async def not_found_error(request):
    attributes = check_display_region(request)
    return jinja.render_template('404.html', request, attributes, status=404)


async def invalid_access_code(request):
    logger.warn('invalid access code entered',
                client_ip=request['client_ip'],
                client_id=request['client_id'],
                trace=request['trace'])
    attributes = check_display_region(request)
    if attributes['display_region'] == 'cy':
        attributes['page_title'] = View.page_title_error_prefix_cy + START_PAGE_TITLE_CY
    else:
        attributes['page_title'] = View.page_title_error_prefix_en + START_PAGE_TITLE_EN
    return jinja.render_template('start.html', request, attributes, status=401)


async def forbidden(request):
    attributes = check_display_region(request)
    attributes['timeout'] = 'true'
    return jinja.render_template('error-forbidden.html', request, attributes, status=403)


async def too_many_requests_eq_launch(request):
    attributes = check_display_region(request)
    await invalidate(request)
    attributes['timeout'] = 'true'
    return jinja.render_template('start-too-many-requests.html', request, attributes, status=429)


async def session_timeout(request, user_journey: str, request_type: str):
    attributes = check_display_region(request)
    attributes['timeout'] = 'true'
    if user_journey == 'start':
        return jinja.render_template('start-timeout.html', request, attributes, status=403)


def setup(app):
    overrides = {
        400: response_error,  # HTTPBadRequest
        401: response_error,  # HTTPUnauthorized
        402: response_error,  # HTTPPaymentRequired
        403: response_error,  # HTTPForbidden
        404: not_found_error,  # HTTPNotFound
        405: response_error,  # HTTPMethodNotAllowed
        406: response_error,  # HTTPNotAcceptable
        407: response_error,  # HTTPProxyAuthenticationRequired
        408: response_error,  # HTTPRequestTimeout
        409: response_error,  # HTTPConflict
        410: response_error,  # HTTPGone
        411: response_error,  # HTTPLengthRequired
        412: response_error,  # HTTPPreconditionFailed
        413: response_error,  # HTTPRequestEntityTooLarge
        414: response_error,  # HTTPRequestURITooLong
        415: response_error,  # HTTPUnsupportedMediaType
        416: response_error,  # HTTPRequestRangeNotSatisfiable
        417: response_error,  # HTTPExpectationFailed
        421: response_error,  # HTTPMisdirectedRequest
        422: response_error,  # HTTPUnprocessableEntity
        424: response_error,  # HTTPFailedDependency
        426: response_error,  # HTTPUpgradeRequired
        428: response_error,  # HTTPPreconditionRequired
        429: response_error,  # HTTPTooManyRequests
        431: response_error,  # HTTPRequestHeaderFieldsTooLarge
        451: response_error,  # HTTPUnavailableForLegalReasons
        500: response_error,  # HTTPInternalServerError
        501: response_error,  # HTTPNotImplemented
        502: response_error,  # HTTPBadGateway
        503: response_error,  # HTTPServiceUnavailable
        504: response_error,  # HTTPGatewayTimeout
        505: response_error,  # HTTPVersionNotSupported
        506: response_error,  # HTTPVariantAlsoNegotiates
        507: response_error,  # HTTPInsufficientStorage
        510: response_error,  # HTTPNotExtended
        511: response_error,  # HTTPNetworkAuthenticationRequired
    }
    error_middleware = create_error_middleware(overrides)
    # This error handling middleware must set its self up first in the chain of middlewares
    # so that it can handle errors throughout the middlewares
    app.middlewares.insert(0, error_middleware)


def check_display_region(request):
    path_prefix = request.app['URL_PATH_PREFIX']

    def path_starts_with(suffix):
        return request.path.startswith(path_prefix + suffix)

    domain_url_en = request.app['DOMAIN_URL_PROTOCOL'] + request.app[
        'DOMAIN_URL_EN']

    base_attributes = {
        'domain_url_en': domain_url_en,
        'page_url': View.gen_page_url(request)
    }

    if path_starts_with('/cy'):
        return {
            **base_attributes,
            'display_region': 'cy',
            'locale': 'cy',
            'page_title': 'PLACEHOLDER WELSH Gwall',
            'contact_us_link': View.get_campaign_site_link(request, 'cy', 'contact-us')
        }
    else:
        return {
            **base_attributes,
            'display_region': 'en',
            'page_title': 'Error',
            'contact_us_link': View.get_campaign_site_link(request, 'en', 'contact-us')
        }


def _get_site_name(attributes, request):
    if attributes['display_region'] == 'cy':
        attributes['site_name_cy'] = request.app['SITE_NAME_CY']
    else:
        attributes['site_name_en'] = request.app['SITE_NAME_EN']
