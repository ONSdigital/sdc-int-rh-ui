from importlib import reload
from unittest import TestCase, mock

from aiohttp.test_utils import AioHTTPTestCase
from aiohttp.web_app import Application
from aiohttp_session import SimpleCookieStorage
from aiohttp_session import session_middleware
from envparse import ConfigurationError, env

from app import session
from app.app import create_app


class TestCreateApp(AioHTTPTestCase):
    config = 'TestingConfig'

    def session_storage(self, app_config):
        self.assertIn('REDIS_SERVER', app_config)
        self.assertIn('REDIS_PORT', app_config)
        self.assertIn('SESSION_AGE', app_config)
        return session_middleware(
            SimpleCookieStorage(cookie_name='RH_SESSION'))

    async def get_application(self):
        # Monkey patch the session setup function to remove Redis dependency for unit tests
        session.setup = self.session_storage
        return create_app(self.config)

    async def test_create_app(self):
        self.assertIsInstance(self.app, Application)

    async def test_security_headers(self):
        nonce = '123456'

        with mock.patch('app.security.get_random_string') as mocked_rando:
            mocked_rando.return_value = nonce
            response = await self.client.request('GET', '/')

        self.assertEqual(response.headers['Strict-Transport-Security'],
                         'max-age=31536000; includeSubDomains')
        self.assertIn("default-src 'self' https://cdn.ons.gov.uk",
                      response.headers['Content-Security-Policy'])
        self.assertIn(
            f"script-src 'self' https://cdn.ons.gov.uk 'nonce-{nonce}'",
            response.headers['Content-Security-Policy'])
        self.assertIn(
            "connect-src 'self' https://cdn.ons.gov.uk",
            response.headers['Content-Security-Policy'])
        self.assertIn(
            "img-src 'self' data: https://cdn.ons.gov.uk",
            response.headers['Content-Security-Policy'])
        self.assertEqual(response.headers['X-Content-Type-Options'], 'nosniff')
        self.assertIn("default-src 'self' https://cdn.ons.gov.uk",
                      response.headers['X-Content-Security-Policy'])
        self.assertEqual(response.headers['Referrer-Policy'], 'strict-origin-when-cross-origin')
        self.assertEqual(response.headers['X-Permitted-Cross-Domain-Policies'], 'None')

        self.assertEqual(response.headers['clear-site-data'], '"storage"')
        self.assertEqual(response.headers['Cross-Origin-Opener-Policy'], 'same-origin')
        self.assertEqual(response.headers['Cross-Origin-Resource-Policy'], 'same-site')
        self.assertEqual(response.headers['Cache-Control'], 'no-store max-age=0')
        self.assertEqual(response.headers['Server'], 'Office For National Statistics')
        self.assertEqual(response.headers['Permissions-Policy'],
                         'accelerometer=(),autoplay=(),camera=(),display-capture=(),document-domain=(),'
                         'encrypted-media=(),fullscreen=(),geolocation=(),gyroscope=(),magnetometer=(),microphone=('
                         '),midi=(),payment=(),picture-in-picture=(),publickey-credentials-get=(),screen-wake-lock=('
                         '),sync-xhr=(self),usb=(),xr-spatial-tracking=()')


class TestCreateAppURLPathPrefix(TestCase):
    config = 'TestingConfig'

    def test_create_app_with_url_path_prefix_en(self):
        from app import config

        url_prefix = '/url-path-prefix'
        config.TestingConfig.URL_PATH_PREFIX = url_prefix

        app = create_app(self.config)
        self.assertEqual(app['URL_PATH_PREFIX'], url_prefix)

        self.assertEqual(app.router['Start:get'].canonical.replace('{display_region}', 'en'),
                         '/url-path-prefix/en/start/')
        self.assertEqual(app.router['Start:post'].canonical.replace('{display_region}', 'en'),
                         '/url-path-prefix/en/start/')
        self.assertEqual(app.router['Info:get'].canonical, '/info')

    def test_create_app_without_url_path_prefix_en(self):
        from app import config

        config.TestingConfig.URL_PATH_PREFIX = ''

        app = create_app(self.config)
        self.assertEqual(app['URL_PATH_PREFIX'], '')

        self.assertEqual(app.router['Start:get'].canonical.replace('{display_region}', 'en'), '/en/start/')
        self.assertEqual(app.router['Start:post'].canonical.replace('{display_region}', 'en'), '/en/start/')
        self.assertEqual(app.router['Info:get'].canonical, '/info')


class TestCreateAppMissingConfig(TestCase):
    config = 'ProductionConfig'
    env_file = 'tests/test_data/local.env'

    def test_create_prod_app(self):
        from app import config

        with self.assertRaises(ConfigurationError) as ex:
            create_app(self.config)
        self.assertIn('not set', ex.exception.args[0])

        env.read_envfile(self.env_file)
        reload(config)
        self.assertIsInstance(create_app(self.config), Application)
