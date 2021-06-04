from .helpers import TestHelpers
from aiohttp.test_utils import unittest_run_loop
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
        self.assertIn(self.get_logo(display_region if display_region else 'ni'), contents)
        if display_region == 'cy':
            self.assertNotIn(self.content_start_exit_button_cy, contents)

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
        self.assertIn(self.get_logo(display_region if display_region else 'ni'), contents)
        if display_region == 'cy':
            self.assertNotIn(self.content_start_exit_button_cy, contents)
            self.assertIn(self.content_start_forbidden_title_cy, contents)
            self.assertIn(self.content_start_timeout_forbidden_link_text_cy, contents)
        else:
            self.assertNotIn(self.content_start_exit_button_en, contents)
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
            self.assertIn(self.get_logo(display_region), contents)
            if display_region == 'cy':
                self.assertIn(self.content_start_exit_button_cy, contents)
                self.assertIn(self.content_start_confirm_address_page_title_cy, contents)
                self.assertIn(self.content_start_confirm_address_title_cy, contents)
            else:
                if display_region == 'en':
                    self.assertIn(self.content_start_exit_button_en, contents)
                self.assertIn(self.content_start_confirm_address_page_title_en, contents)
                self.assertIn(self.content_start_confirm_address_title_en, contents)

            request_url = self.get_url_from_class('RequestEnterAddress', 'get', display_region, 'access-code')
            confirm_url = self.get_url_from_class('StartConfirmAddress', 'post', display_region)

            response = await self.client.request('GET', request_url)
            self.assertLogEvent(cm, "received GET on endpoint '" + display_region +
                                "/request/access-code/enter-address'")

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            self.check_text_enter_address(display_region, contents, check_empty=False, check_error=False)

            response = await self.client.request('POST', confirm_url, data=self.start_confirm_address_data_yes)
            self.assertEqual(response.status, 403)
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            if display_region == 'cy':
                self.assertNotIn(self.content_start_exit_button_cy, contents)
                self.assertIn(self.content_start_forbidden_title_cy, contents)
                self.assertIn(self.content_start_timeout_forbidden_link_text_cy, contents)
            else:
                self.assertNotIn(self.content_start_exit_button_en, contents)
                self.assertIn(self.content_start_forbidden_title_en, contents)
                self.assertIn(self.content_start_timeout_forbidden_link_text_en, contents)

    @unittest_run_loop
    async def test_no_direct_access_no_session_start_confirm_address(self):
        await self.assert_no_session('StartConfirmAddress', 'GET', 'en')
        await self.assert_no_session('StartConfirmAddress', 'GET', 'cy')
        await self.assert_no_session('StartConfirmAddress', 'POST', 'en')
        await self.assert_no_session('StartConfirmAddress', 'POST', 'cy')

    @unittest_run_loop
    async def test_forbidden_start_confirm_address(self):
        await self.assert_forbidden('StartConfirmAddress', 'GET', 'en')
        await self.assert_forbidden('StartConfirmAddress', 'GET', 'cy')
        await self.assert_forbidden('StartConfirmAddress', 'POST', 'en')
        await self.assert_forbidden('StartConfirmAddress', 'POST', 'cy')

    @unittest_run_loop
    async def test_no_direct_access_no_session_request_common_enter_address(self):
        await self.assert_no_session('RequestEnterAddress', 'POST', 'en', 'access-code')
        await self.assert_no_session('RequestEnterAddress', 'POST', 'cy', 'access-code')

    @unittest_run_loop
    async def test_no_direct_access_no_session_request_common_select_address(self):
        await self.assert_no_session('RequestSelectAddress', 'GET', 'en', 'access-code')
        await self.assert_no_session('RequestSelectAddress', 'GET', 'cy', 'access-code')
        await self.assert_no_session('RequestSelectAddress', 'POST', 'en', 'access-code')
        await self.assert_no_session('RequestSelectAddress', 'POST', 'cy', 'access-code')

    @unittest_run_loop
    async def test_no_direct_access_no_session_request_common_confirm_address(self):
        await self.assert_no_session('RequestConfirmAddress', 'GET', 'en', 'access-code')
        await self.assert_no_session('RequestConfirmAddress', 'GET', 'cy', 'access-code')
        await self.assert_no_session('RequestConfirmAddress', 'POST', 'en', 'access-code')
        await self.assert_no_session('RequestConfirmAddress', 'POST', 'cy', 'access-code')

    @unittest_run_loop
    async def test_no_direct_access_no_session_request_code_select_how_to_receive(self):
        await self.assert_no_session('RequestCodeSelectHowToReceive', 'GET', 'en', request_type='access-code')
        await self.assert_no_session('RequestCodeSelectHowToReceive', 'GET', 'cy', request_type='access-code')
        await self.assert_no_session('RequestCodeSelectHowToReceive', 'POST', 'en', request_type='access-code')
        await self.assert_no_session('RequestCodeSelectHowToReceive', 'POST', 'cy', request_type='access-code')

    @unittest_run_loop
    async def test_no_direct_access_no_session_request_code_enter_mobile(self):
        await self.assert_no_session('RequestCodeEnterMobile', 'GET', 'en', request_type='access-code')
        await self.assert_no_session('RequestCodeEnterMobile', 'GET', 'cy', request_type='access-code')
        await self.assert_no_session('RequestCodeEnterMobile', 'POST', 'en', request_type='access-code')
        await self.assert_no_session('RequestCodeEnterMobile', 'POST', 'cy', request_type='access-code')

    @unittest_run_loop
    async def test_no_direct_access_no_session_request_code_confirm_send_by_text(self):
        await self.assert_no_session('RequestCodeConfirmSendByText', 'GET', 'en', request_type='access-code')
        await self.assert_no_session('RequestCodeConfirmSendByText', 'GET', 'cy', request_type='access-code')
        await self.assert_no_session('RequestCodeConfirmSendByText', 'POST', 'en', request_type='access-code')
        await self.assert_no_session('RequestCodeConfirmSendByText', 'POST', 'cy', request_type='access-code')

    @unittest_run_loop
    async def test_no_direct_access_no_session_request_common_enter_name(self):
        await self.assert_no_session('RequestCommonEnterName', 'GET', 'en', request_type='access-code')
        await self.assert_no_session('RequestCommonEnterName', 'GET', 'cy', request_type='access-code')
        await self.assert_no_session('RequestCommonEnterName', 'POST', 'en', request_type='access-code')
        await self.assert_no_session('RequestCommonEnterName', 'POST', 'cy', request_type='access-code')

    @unittest_run_loop
    async def test_no_direct_access_no_session_request_common_confirm_send_by_post(self):
        await self.assert_no_session('RequestCommonConfirmSendByPost', 'GET', 'en', request_type='access-code')
        await self.assert_no_session('RequestCommonConfirmSendByPost', 'GET', 'cy', request_type='access-code')
        await self.assert_no_session('RequestCommonConfirmSendByPost', 'POST', 'en', request_type='access-code')
        await self.assert_no_session('RequestCommonConfirmSendByPost', 'POST', 'cy', request_type='access-code')

    @unittest_run_loop
    async def test_no_direct_access_no_session_request_code_sent_by_text(self):
        await self.assert_no_session('RequestCodeSentByText', 'GET', 'en', request_type='access-code')
        await self.assert_no_session('RequestCodeSentByText', 'GET', 'cy', request_type='access-code')

    @unittest_run_loop
    async def test_no_direct_access_no_session_request_code_sent_by_post(self):
        await self.assert_no_session('RequestCodeSentByPost', 'GET', 'en', request_type='access-code')
        await self.assert_no_session('RequestCodeSentByPost', 'GET', 'cy', request_type='access-code')

    @unittest_run_loop
    async def test_session_start_to_fulfilment_to_start(self):
        await self.assert_cross_journey_forbidden('en', 'E')
        await self.assert_cross_journey_forbidden('en', 'W')
        await self.assert_cross_journey_forbidden('cy', 'W')
