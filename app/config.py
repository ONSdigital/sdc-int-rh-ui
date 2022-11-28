from functools import partial

from envparse import Env, ConfigurationError


class Config(dict):

    CONFIG_NAME = Env().str('CONFIG_NAME', default='BaseConfig')

    def from_object(self, obj):
        for key in dir(obj):
            if key.isupper():
                config = getattr(obj, key)
                if config is None:
                    raise ConfigurationError(f'{key} not set')
                self[key] = config

    def get_service_urls_mapped_with_path(self,
                                          path='/',
                                          suffix='URL',
                                          excludes=None) -> dict:
        return {
            service_name: f'{self[service_name]}{path}'
            for service_name in self
            if service_name.endswith(suffix) and service_name not in (
                excludes if excludes else [])
        }

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(f'"{name}" not found')

    def __setattr__(self, name, value):
        self[name] = value


class BaseConfig:
    env = Env()
    env = partial(env, default=None)

    HOST = env('HOST')
    PORT = env('PORT')
    DEBUG = env('DEBUG', cast=bool, default=False)
    LOG_LEVEL = env('LOG_LEVEL')
    EXT_LOG_LEVEL = env('EXT_LOG_LEVEL')

    DOMAIN_URL_PROTOCOL = env('DOMAIN_URL_PROTOCOL', default='https://')
    DOMAIN_URL = env('DOMAIN_URL')

    # NB: "ACCOUNT_SERVICE_URL" is actually the RH UI route which is passed in the launch token to allow redirection
    # back to the RH UI "start" page, the name is a hangover from other survey systems
    ACCOUNT_SERVICE_URL = env('ACCOUNT_SERVICE_URL')

    EQ_URL = env('EQ_URL')
    RHSVC_URL = env('RHSVC_URL')

    URL_PATH_PREFIX = env('URL_PATH_PREFIX', default='')

    GTM_CONTAINER_ID = env('GTM_CONTAINER_ID', default='')
    GTM_AUTH = env('GTM_AUTH', default='')

    REDIS_SERVER = env('REDIS_SERVER', default='localhost')

    REDIS_PORT = env('REDIS_PORT', default='6379')
    REDIS_POOL_MIN = env('REDIS_POOL_MIN', default='50')
    REDIS_POOL_MAX = env('REDIS_POOL_MAX', default='500')

    SESSION_AGE = env('SESSION_AGE', default='2700')  # 45 minutes

    SITE_NAME_EN = env('SITE_NAME_EN', default='ONS Surveys')
    SITE_NAME_CY = env('SITE_NAME_CY', default='PLACEHOLDER WELSH ONS Surveys')


class ProductionConfig(BaseConfig):
    pass


class DevelopmentConfig(BaseConfig):
    env = Env()
    HOST = env.str('HOST', default='0.0.0.0')
    PORT = env.int('PORT', default='9092')
    DEBUG = env('DEBUG', cast=bool, default=False)
    LOG_LEVEL = env('LOG_LEVEL', default='INFO')
    EXT_LOG_LEVEL = env('EXT_LOG_LEVEL', default='INFO')

    DOMAIN_URL_PROTOCOL = 'http://'
    DOMAIN_URL = env.str('DOMAIN_URL', default='localhost:9092')

    ACCOUNT_SERVICE_URL = env.str('ACCOUNT_SERVICE_URL',
                                  default='http://localhost:9092')
    EQ_URL = env.str('EQ_URL', default='http://localhost:5000')
    RHSVC_URL = env.str('RHSVC_URL', default='http://localhost:8071')

    URL_PATH_PREFIX = env('URL_PATH_PREFIX', default='')

    GTM_CONTAINER_ID = env.str('GTM_CONTAINER_ID', default='GTM-MRQGCXS')
    GTM_AUTH = env.str('GTM_AUTH', default='SMijm6Rii1nctiBFRb1Rdw')

    REDIS_SERVER = env('REDIS_SERVER', default='localhost')

    REDIS_PORT = env('REDIS_PORT', default='6379')
    REDIS_POOL_MIN = env('REDIS_POOL_MIN', default='50')
    REDIS_POOL_MAX = env('REDIS_POOL_MAX', default='500')

    SESSION_AGE = env('SESSION_AGE', default='2700')  # 45 minutes

    SITE_NAME_EN = env('SITE_NAME_EN', default='ONS Surveys')
    SITE_NAME_CY = env('SITE_NAME_CY', default='PLACEHOLDER WELSH ONS Surveys')


class TestingConfig(DevelopmentConfig):
    HOST = '0.0.0.0'
    PORT = '9092'
    DEBUG = True
    LOG_LEVEL = 'DEBUG'
    EXT_LOG_LEVEL = 'DEBUG'

    DOMAIN_URL_PROTOCOL = 'http://'
    DOMAIN_URL = 'localhost:9092'

    ACCOUNT_SERVICE_URL = 'http://localhost:9092'
    EQ_URL = 'http://localhost:5000'
    RHSVC_URL = 'http://localhost:8071'

    URL_PATH_PREFIX = ''

    GTM_CONTAINER_ID = 'GTM-MRQGCXS'
    GTM_AUTH = 'SMijm6Rii1nctiBFRb1Rdw'

    REDIS_SERVER = ''

    REDIS_PORT = ''
    REDIS_POOL_MIN = '50'
    REDIS_POOL_MAX = '500'

    SESSION_AGE = ''

    SITE_NAME_EN = 'ONS Surveys'
    SITE_NAME_CY = 'PLACEHOLDER WELSH ONS Surveys'
