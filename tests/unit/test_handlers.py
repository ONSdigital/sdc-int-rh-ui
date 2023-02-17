from tests.unit.helpers import TestHelpers


class TestCookiesAndPrivacyHandlers(TestHelpers):

    # Cookies
    async def test_get_cookies_page_en(self):
        with self.assertLogs('respondent-home', 'INFO') as cm:
            response = await self.client.request('GET', self.get_cookies_en)
            self.assertLogEvent(cm, "received GET on endpoint 'en/cookies/'")
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.content_cookies_page_title_en, contents)
            self.assertIn(self.content_cookies_heading_en, contents)
            self.assertIn(self.content_breadcrumbs_back_button_en, contents)
            self.assertSiteLogo('en', contents)

    async def test_get_cookies_page_cy(self):
        with self.assertLogs('respondent-home', 'INFO') as cm:
            response = await self.client.request('GET', self.get_cookies_cy)
            self.assertLogEvent(cm, "received GET on endpoint 'cy/cookies/'")
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.content_cookies_page_title_cy, contents)
            self.assertIn(self.content_cookies_heading_cy, contents)
            self.assertIn(self.content_breadcrumbs_back_button_cy, contents)
            self.assertSiteLogo('cy', contents)

    # PrivacyAndDataProtection
    async def test_get_privacy_page_en(self):
        with self.assertLogs('respondent-home', 'INFO') as cm:
            response = await self.client.request('GET', self.get_privacy_en)
            self.assertLogEvent(cm, "received GET on endpoint 'en/privacy-and-data-protection/'")
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.content_privacy_page_title_en, contents)
            self.assertIn(self.content_privacy_heading_en, contents)
            self.assertIn(self.content_breadcrumbs_back_button_en, contents)
            self.assertSiteLogo('en', contents)

    async def test_get_privacy_page_cy(self):
        with self.assertLogs('respondent-home', 'INFO') as cm:
            response = await self.client.request('GET', self.get_privacy_cy)
            self.assertLogEvent(cm, "received GET on endpoint 'cy/privacy-and-data-protection/'")
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.content_privacy_page_title_cy, contents)
            self.assertIn(self.content_privacy_heading_cy, contents)
            self.assertIn(self.content_breadcrumbs_back_button_cy, contents)
            self.assertSiteLogo('cy', contents)
