import aiohttp_jinja2
import jinja2
from aiohttp import ClientSession, ClientTimeout, TCPConnector
from aiohttp.web import Application
from aiohttp_utils import negotiation, routing
from structlog import get_logger

from app import config, domains, error_handlers, flash, i18n, routes, security, session, trace, google_analytics
from app.app_logging import logger_initial_config

logger = get_logger('respondent-home')


async def on_startup(app):
    # by limiting keep-alive, we help prevent errors during RHSvc scale-back.
    conn = TCPConnector(keepalive_timeout=5)
    app.http_session_pool = ClientSession(connector=conn, timeout=ClientTimeout(total=30), trust_env=True)


async def on_cleanup(app):
    await app.http_session_pool.close()


def jinja_filter_set_attributes(dictionary, attributes):
    for key in attributes:
        dictionary[key] = attributes[key]
    return dictionary


def create_app(config_name=None) -> Application:
    """
    App factory. Sets up routes and all plugins.
    """
    app_config = config.Config()

    # Set the config base
    app_config.from_object(config.Config)

    # NB: raises ConfigurationError if an object attribute is None
    # Allow the config_name argument to override the environment settings, if it is given
    config_name = (config_name or app_config['CONFIG_NAME'])

    # Import the config class specified by the config_name
    app_config.from_object(getattr(config, config_name))

    app = Application(
        debug=app_config['DEBUG'],
        middlewares=[
            # Sets the order of middleware evaluation. Security first, then error handling, then all others
            security.nonce_middleware,
            error_handlers.setup(),
            session.setup(app_config),
            flash.flash_middleware,
            trace.trace_middleware
        ],
        router=routing.ResourceRouter(),
    )

    # Store upper-cased configuration variables on app
    app.update(app_config)

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
            flash.context_processor,
            aiohttp_jinja2.request_processor,
            google_analytics.ga_ua_id_processor,
            domains.domain_processor,
            security.context_processor
        ],
        extensions=['app.i18n.i18n'])

    env.filters['setAttributes'] = jinja_filter_set_attributes
    env.install_gettext_translations(i18n, newstyle=True)

    app.on_startup.append(on_startup)
    app.on_cleanup.append(on_cleanup)
    app.on_response_prepare.append(security.on_prepare)

    logger.info('app setup complete', config=config_name)

    return app
