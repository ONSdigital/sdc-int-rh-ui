import os


class Config(object):
    PROTOCOL = os.getenv('PROTOCOL', 'http')
    INFO = '/info'

    RESPONDENT_USERNAME = os.getenv('RESPONDENT_USERNAME', 'example@example.com')
    RESPONDENT_PASSWORD = os.getenv('RESPONDENT_PASSWORD', 'password')

    INTERNAL_USERNAME = os.getenv('INTERNAL_USERNAME', 'uaa_user')
    INTERNAL_PASSWORD = os.getenv('INTERNAL_PASSWORD', 'password')

    DJANGO_SERVICE_HOST = os.getenv('DJANGO_SERVICE_HOST', 'localhost')
    DJANGO_SERVICE_PORT = os.getenv('DJANGO_SERVICE_PORT', 8040)
    DJANGO_SERVICE = f'{PROTOCOL}://{DJANGO_SERVICE_HOST}:{DJANGO_SERVICE_PORT}'

    FRONTSTAGE_SERVICE_HOST = os.getenv('FRONTSTAGE_SERVICE_HOST', 'localhost')
    FRONTSTAGE_SERVICE_PORT = os.getenv('FRONTSTAGE_SERVICE_PORT', 8082)
    FRONTSTAGE_SERVICE = f'{PROTOCOL}://{FRONTSTAGE_SERVICE_HOST}:{FRONTSTAGE_SERVICE_PORT}'

    RHSVC_SERVICE_HOST = os.getenv('RHSVC_SERVICE_HOST', 'localhost')
    RHSVC_SERVICE_PORT = os.getenv('RHSVC_SERVICE_PORT', 8071)
    RHSVC_SERVICE = f'{PROTOCOL}://{RHSVC_SERVICE_HOST}:{RHSVC_SERVICE_PORT}'

    NOTIFY_GATEWAY_SERVICE_HOST = os.getenv('NOTIFY_GATEWAY_SERVICE_HOST', 'localhost')
    NOTIFY_GATEWAY_SERVICE_PORT = os.getenv('NOTIFY_GATEWAY_SERVICE_PORT', 8181)
    NOTIFY_GATEWAY_SERVICE = f'{PROTOCOL}://{NOTIFY_GATEWAY_SERVICE_HOST}:{NOTIFY_GATEWAY_SERVICE_PORT}'

    SECURE_MESSAGE_SERVICE_HOST = os.getenv('SECURE_MESSAGE_SERVICE_HOST', 'localhost')
    SECURE_MESSAGE_SERVICE_PORT = os.getenv('SECURE_MESSAGE_SERVICE_PORT', 5050)
    SECURE_MESSAGE_SERVICE = f'{PROTOCOL}://{SECURE_MESSAGE_SERVICE_HOST}:{SECURE_MESSAGE_SERVICE_PORT}'

    SECURITY_USER_NAME = os.getenv('SECURITY_USER_NAME', 'admin')
    SECURITY_USER_PASSWORD = os.getenv('SECURITY_USER_PASSWORD', 'secret')
    BASIC_AUTH = (SECURITY_USER_NAME, SECURITY_USER_PASSWORD)

    OAUTH_CLIENT_ID = os.getenv('OAUTH_CLIENT_ID', 'ons@ons.gov')
    OAUTH_CLIENT_SECRET = os.getenv('OAUTH_CLIENT_SECRET', 'password')

    DATABASE_URI = os.getenv('DATABASE_URI', 'postgres://postgres:postgres@localhost:6432/postgres')
    DJANGO_OAUTH_DATABASE_URI = os.getenv('DJANGO_OAUTH_DATABASE_URI', DATABASE_URI)
    PARTY_DATABASE_URI = os.getenv('PARTY_DATABASE_URI', DATABASE_URI)
    COLLECTION_INSTRUMENT_DATABASE_URI = os.getenv('COLLECTION_INSTRUMENT_DATABASE_URI', DATABASE_URI)
    SECURE_MESSAGE_DATABASE_URI = os.getenv('SECURE_MESSAGE_DATABASE_URI', DATABASE_URI)

    EQ_SURVEY_RUNNER_HOST = os.getenv('EQ_SURVEY_RUNNER_HOST', 'localhost')
    EQ_SURVEY_RUNNER_PORT = os.getenv('EQ_SURVEY_RUNNER_PORT', 5000)
    EQ_SURVEY_RUNNER_URL = f'{PROTOCOL}://{EQ_SURVEY_RUNNER_HOST}:{EQ_SURVEY_RUNNER_PORT}'

    RESPONDENT_HOME_HOST = os.getenv('RESPONDENT_HOME_HOST', 'localhost')
    RESPONDENT_HOME_PORT = os.getenv('RESPONDENT_HOME_PORT', 9092)
    RESPONDENT_HOME_SERVICE = f'{PROTOCOL}://{RESPONDENT_HOME_HOST}:{RESPONDENT_HOME_PORT}'
