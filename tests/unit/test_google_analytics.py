from aiohttp.test_utils import make_mocked_request

from app.google_analytics import ga_ua_id_processor
from tests.unit import RHTestCase


class TestGoogleAnalytics(RHTestCase):
    async def test_google_analytics_context(self):
        self.app['GTM_CONTAINER_ID'] = 'GTM-XXXXXXX'
        self.app['GTM_TAG_ID'] = '12345'
        request = make_mocked_request('GET', '/', app=self.app)
        context = await ga_ua_id_processor(request)
        self.assertEqual(context['gtm_cont_id'], 'GTM-XXXXXXX')
        self.assertEqual(context['gtm_tag_id'], '12345')

    async def test_google_analytics_script_rendered_base_en(self):
        self.app['GTM_CONTAINER_ID'] = 'GTM-XXXXXXX'
        self.app['GTM_TAG_ID'] = 'G-1234567890'
        response = await self.client.request('GET', self.get_start_en)
        self.assertEqual(response.status, 200)
        response = await response.content.read()
        self.assertIn("(window,document,\'script\',\'dataLayer\',\'GTM-XXXXXXX\');".encode(), response)
        self.assertIn("https://www.googletagmanager.com/gtag/js?id=G-1234567890".encode(), response)

    async def test_google_analytics_script_rendered_base_cy(self):
        self.app['GTM_CONTAINER_ID'] = 'GTM-XXXXXXX'
        self.app['GTM_TAG_ID'] = '12345'
        response = await self.client.request('GET', self.get_start_cy)
        self.assertEqual(response.status, 200)
        response = await response.content.read()
        self.assertIn("(window,document,\'script\',\'dataLayer\',\'GTM-XXXXXXX\');".encode(), response)
        self.assertIn("https://www.googletagmanager.com/gtag/js?id=12345".encode(), response)

    async def test_google_analytics_script_not_rendered_missing_container_id_base_en(self):
        self.app['GTM_CONTAINER_ID'] = ''

        response = await self.client.request('GET', self.get_start_en)
        self.assertEqual(response.status, 200)
        self.assertNotIn("(window,document,\'script\',\'dataLayer\',\'GTM-XXXXXXX\');".encode(),
                         await response.content.read())

    async def test_google_analytics_script_not_rendered_missing_container_id_base_cy(self):
        self.app['GTM_CONTAINER_ID'] = ''

        response = await self.client.request('GET', self.get_start_cy)
        self.assertEqual(response.status, 200)
        self.assertNotIn("(window,document,\'script\',\'dataLayer\',\'GTM-XXXXXXX\');".encode(),
                         await response.content.read())

    async def test_google_analytics_script_not_rendered_base_en(self):
        self.app['GTM_TAG_ID'] = ''

        response = await self.client.request('GET', self.get_start_en)
        self.assertEqual(response.status, 200)
        self.assertNotIn("https://www.googletagmanager.com/gtag/js?id=12345".encode(), await response.content.read())

    async def test_google_analytics_script_not_rendered_base_cy(self):
        self.app['GTM_TAG_ID'] = ''

        response = await self.client.request('GET', self.get_start_cy)
        self.assertEqual(response.status, 200)
        self.assertNotIn("https://www.googletagmanager.com/gtag/js?id=12345".encode(), await response.content.read())
