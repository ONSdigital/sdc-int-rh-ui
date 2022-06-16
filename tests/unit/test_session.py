from .helpers import TestHelpers
from aioresponses import aioresponses


class TestSessionHandling(TestHelpers):

    def clear_session(self):
        """
        Ensure session cleared from previous requests
        """
        jar = self.client._session.cookie_jar
        jar.clear()

    def build_url(self, class_name, method, display_region=None, request_type=''):
        if not display_region:
            url = self.app.router[class_name + ':' + method.lower()].url_for()
        else:
            url = self.app.router[class_name + ':' + method.lower()].url_for(
                display_region=display_region, request_type=request_type)
        return url

    async def assert_no_session(
            self, class_name, method, display_region=None, request_type=''):
        url = self.build_url(class_name, method, display_region, request_type)
        self.clear_session()
        with self.assertLogs('respondent-home', 'WARN') as cm:
            if method == 'POST':
                response = await self.client.request('POST', url, allow_redirects=False)
            else:
                response = await self.client.request('GET', url, allow_redirects=False)
        self.assertLogEvent(cm, 'session timed out')
        self.assertEqual(response.status, 403)
        contents = str(await response.content.read())
        self.assertSiteLogo(display_region, contents)
        self.assertNotExitButton(display_region, contents)
        if display_region == 'cy':
            if 'start' in url.path:
                self.assertIn(self.content_start_timeout_title_cy, contents)
                self.assertIn(self.content_start_timeout_bullet_one_cy, contents)
                self.assertIn(self.content_start_timeout_bullet_two_cy, contents)
                self.assertIn(self.content_start_timeout_link_text_cy, contents)
            else:
                self.assertIn(self.content_request_timeout_title_cy, contents)
                self.assertIn(self.content_request_timeout_bullet_one_cy, contents)
                self.assertIn(self.content_request_code_timeout_bullet_two_cy, contents)
                self.assertIn(self.content_request_code_timeout_link_text_cy, contents)
        else:
            self.assertIn(self.content_start_timeout_bullet_one_en, contents)
            if 'start' in url.path:
                self.assertIn(self.content_start_timeout_title_en, contents)
                self.assertIn(self.content_start_timeout_bullet_one_en, contents)
                self.assertIn(self.content_start_timeout_bullet_two_en, contents)
                self.assertIn(self.content_start_timeout_link_text_en, contents)
            else:
                self.assertIn(self.content_request_timeout_title_en, contents)
                self.assertIn(self.content_request_timeout_bullet_one_en, contents)
                self.assertIn(self.content_request_code_timeout_bullet_two_en, contents)
                self.assertIn(self.content_request_code_timeout_link_text_en, contents)

    async def assert_forbidden(
            self, class_name, method, display_region=None, request_type=''):
        url = self.build_url(class_name, method, display_region, request_type)
        self.clear_session()
        cookie = {'RH_SESSION': '{ "session": {"client_id": "36be6b97-b4de-4718-8a74-8b27fb03ca8c"}}'}
        header = {"X-Cloud-Trace-Context": "0123456789/0123456789012345678901;o=1"}
        with self.assertLogs('respondent-home', 'WARN') as cm:
            if method == 'POST':
                response = await self.client.request('POST', url, allow_redirects=False, cookies=cookie, headers=header)
            else:
                response = await self.client.request('GET', url, allow_redirects=False, cookies=cookie,  headers=header)
        self.assertLogEvent(cm, 'permission denied',
                            client_id='36be6b97-b4de-4718-8a74-8b27fb03ca8c', trace='0123456789')
        self.assertEqual(response.status, 403)
        contents = str(await response.content.read())
        self.assertSiteLogo(display_region, contents)
        self.assertNotExitButton(display_region, contents)
        if display_region == 'cy':
            self.assertIn(self.content_start_forbidden_title_cy, contents)
            self.assertIn(self.content_start_timeout_forbidden_link_text_cy, contents)
        else:
            self.assertIn(self.content_start_forbidden_title_en, contents)
            self.assertIn(self.content_start_timeout_forbidden_link_text_en, contents)

    async def assert_cross_journey_forbidden(self, display_region, region):

        if region == 'W':
            uac_payload = self.uac_json_w
        else:
            uac_payload = self.uac_json_e
        with self.assertLogs('respondent-home', 'INFO') as cm, \
                aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=uac_payload)
            response = await self.client.request('POST', self.get_url_from_class('Start', 'post', display_region),
                                                 allow_redirects=True, data=self.start_data_valid)

            self.assertLogEvent(cm, "received POST on endpoint '" + display_region + "/start'")
            self.assertLogEvent(cm, "received GET on endpoint '" + display_region + "/start/confirm-address'")
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertSiteLogo(display_region, contents)
            self.assertExitButton(display_region, contents)
            if display_region == 'cy':
                self.assertIn(self.content_start_confirm_address_page_title_cy, contents)
                self.assertIn(self.content_start_confirm_address_title_cy, contents)
            else:
                self.assertIn(self.content_start_confirm_address_page_title_en, contents)
                self.assertIn(self.content_start_confirm_address_title_en, contents)

            request_url = self.get_url_from_class('RequestEnterAddress', 'get', display_region, 'access-code')
            confirm_url = self.get_url_from_class('StartConfirmAddress', 'post', display_region)

            response = await self.client.request('GET', request_url)
            self.assertLogEvent(cm, "received GET on endpoint '" + display_region +
                                "/request/access-code/enter-address'")

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.check_text_enter_address(display_region, contents, check_empty=False, check_error=False)

            response = await self.client.request('POST', confirm_url, data=self.start_confirm_address_data_yes)
            self.assertEqual(response.status, 403)
            contents = str(await response.content.read())
            self.assertSiteLogo(display_region, contents)
            self.assertNotExitButton(display_region, contents)
            if display_region == 'cy':
                self.assertIn(self.content_start_forbidden_title_cy, contents)
                self.assertIn(self.content_start_timeout_forbidden_link_text_cy, contents)
            else:
                self.assertIn(self.content_start_forbidden_title_en, contents)
                self.assertIn(self.content_start_timeout_forbidden_link_text_en, contents)

    async def test_no_direct_access_no_session_start_confirm_address(self):
        await self.assert_no_session('StartConfirmAddress', 'GET', 'en')
        await self.assert_no_session('StartConfirmAddress', 'GET', 'cy')
        await self.assert_no_session('StartConfirmAddress', 'POST', 'en')
        await self.assert_no_session('StartConfirmAddress', 'POST', 'cy')

    async def test_forbidden_start_confirm_address(self):
        await self.assert_forbidden('StartConfirmAddress', 'GET', 'en')
        await self.assert_forbidden('StartConfirmAddress', 'GET', 'cy')
        await self.assert_forbidden('StartConfirmAddress', 'POST', 'en')
        await self.assert_forbidden('StartConfirmAddress', 'POST', 'cy')
