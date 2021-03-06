import types

import aiohttp_jinja2
import jinja2
from aiohttp import BasicAuth, ClientSession, ClientTimeout, TCPConnector
from aiohttp.client_exceptions import (ClientConnectionError,
                                       ClientConnectorError,
                                       ClientResponseError)
from aiohttp.web import Application
from aiohttp_utils import negotiation, routing
from structlog import get_logger
from app import i18n

from . import config
from . import error_handlers
from . import flash
from . import domains
from . import routes
from . import security
from . import session
from . import settings
from . import trace
from .app_logging import logger_initial_config

logger = get_logger('respondent-home')


async def on_startup(app):
    # by limiting keep-alive, we help prevent errors during RHSvc scale-back.
    conn = TCPConnector(keepalive_timeout=5)
    app.http_session_pool = ClientSession(connector=conn, timeout=ClientTimeout(total=30), trust_env=True)


async def on_cleanup(app):
    await app.http_session_pool.close()


async def check_services(app: Application) -> bool:
    for service_name in app.service_status_urls:
        url = app.service_status_urls[service_name]
        logger.info('making health check get request', url=url)
        try:
            async with app.http_session_pool.get(url) as resp:
                resp.raise_for_status()
        except (ClientConnectorError, ClientConnectionError,
                ClientResponseError):
            logger.error('failed to connect to required service',
                         config=service_name,
                         url=url)
            return False
    else:
        logger.info('all required services are healthy')
        return True


def jinja_filter_set_attributes(dictionary, attributes):
    for key in attributes:
        dictionary[key] = attributes[key]
    return dictionary


def create_app(config_name=None) -> Application:
    """
    App factory. Sets up routes and all plugins.
    """
    app_config = config.Config()
    app_config.from_object(settings)

    # NB: raises ConfigurationError if an object attribute is None
    config_name = (config_name or app_config['ENV'])
    app_config.from_object(getattr(config, config_name))

    # Create basic auth for services
    [
        app_config.__setitem__(key, BasicAuth(*app_config[key]))
        for key in app_config if key.endswith('_AUTH') and not key == "GTM_AUTH"
    ]

    app = Application(
        debug=settings.DEBUG,
        middlewares=[
            security.nonce_middleware,
            session.setup(app_config),
            flash.flash_middleware,
            trace.trace_middleware
        ],
        router=routing.ResourceRouter(),
    )

    # Handle 500 errors
    error_handlers.setup(app)

    # Store upper-cased configuration variables on app
    app.update(app_config)

    # Store a dict of health check urls for required services
    app.service_status_urls = app_config.get_service_urls_mapped_with_path(
        path='/info',
        excludes=[
            'ACCOUNT_SERVICE_URL', 'EQ_URL', 'WEBCHAT_SVC_URL',
            'ADDRESS_INDEX_SVC_URL', 'ADDRESS_INDEX_SVC_EXTERNAL_URL', 'AD_LOOK_UP_SVC_URL'
        ])

    # Monkey patch the check_services function as a method to the app object
    app.check_services = types.MethodType(check_services, app)

    # Bind logger
    logger_initial_config(log_level=app['LOG_LEVEL'],
                          ext_log_level=app['EXT_LOG_LEVEL'])

    # Set up routes
    routes.setup(app, url_path_prefix=app['URL_PATH_PREFIX'])

    # Use content negotiation middleware to render JSON responses
    negotiation.setup(app)

    # Setup jinja2 environment
    env = aiohttp_jinja2.setup(
        app,
        loader=jinja2.PackageLoader('app', 'templates'),
        context_processors=[
            flash.context_processor, aiohttp_jinja2.request_processor, domains.domain_processor, security.context_processor
        ],
        extensions=['app.i18n.i18n'])

    env.filters['setAttributes'] = jinja_filter_set_attributes
    env.install_gettext_translations(i18n, newstyle=True)

    app.on_startup.append(on_startup)
    app.on_cleanup.append(on_cleanup)
    app.on_response_prepare.append(security.on_prepare)

    logger.info('app setup complete', config=config_name)

    return app
