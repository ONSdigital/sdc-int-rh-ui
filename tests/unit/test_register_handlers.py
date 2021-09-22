from aiohttp.test_utils import unittest_run_loop

from .helpers import TestHelpers


# noinspection PyTypeChecker
class TestWebFormHandlers(TestHelpers):
    user_journey = 'register'
    display_region = 'en'

    def check_content_register(self, display_region, contents):
        self.assertCorrectHeadTitleTag(display_region, 'Take part in a survey', contents, error=False)
        self.assertSiteLogo(display_region, contents)
        self.assertNotExitButton(display_region, contents)
        self.assertCorrectPageTitle('Take part in a survey', contents)
        self.assertIn('How to register a child', contents)

    async def get_register(self, display_region):
        with self.assertLogs('respondent-home', 'INFO') as cm:
            get_response = await self.client.request('GET', self.get_register_en)
            self.assertLogEvent(cm, self.build_url_log_entry('register', display_region, 'GET',
                                                             include_request_type=False, include_page=False))
            self.assertEqual(get_response.status, 200)
            self.check_content_register(display_region, str(await get_response.content.read()))

    @unittest_run_loop
    async def test_register(self):
        await self.get_register('en')
