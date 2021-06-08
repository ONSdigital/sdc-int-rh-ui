from unittest import mock

from aiohttp.client_exceptions import ClientConnectionError
from aioresponses import aioresponses

from . import RHTestCase

attempts_retry_limit = 5


# noinspection PyTypeChecker
class TestHelpers(RHTestCase):
    # Tests of pages/steps in all paths

    user_journey = ''
    request_type = ''

    def get_logo(self, display_region):
        if display_region == 'cy':
            logo = self.ons_logo_cy
        else:
            logo = self.ons_logo_en
        return logo

    def build_url_log_entry(self, page, display_region, request_type, include_request_type=True, include_page=True):
        if not include_page:
            link = "received " + request_type + " on endpoint '" + display_region + "/" + self.user_journey
        elif not include_request_type:
            link = "received " + request_type + " on endpoint '" + display_region + "/" + self.user_journey + "/" + \
                   page + "'"
        else:
            link = "received " + request_type + " on endpoint '" + display_region + "/" + self.user_journey + "/" + \
                   self.request_type + "/" + page + "'"
        return link

    def build_translation_link(self, page, display_region, include_request_type=True, include_page=True):
        if display_region == 'cy':
            if not include_page:
                link = '<a href="/en/' + self.user_journey + '/" lang="en" >English</a>'
            elif not include_request_type:
                link = '<a href="/en/' + self.user_journey + '/' + page + '/" lang="en" >English</a>'
            else:
                link = '<a href="/en/' + self.user_journey + '/' + self.request_type + '/' + page + \
                       '/" lang="en" >English</a>'
        else:
            if not include_page:
                link = '<a href="/cy/' + self.user_journey + '/" lang="cy" >Cymraeg</a>'
            elif not include_request_type:
                link = '<a href="/cy/' + self.user_journey + '/' + page + '/" lang="cy" >Cymraeg</a>'
            else:
                link = '<a href="/cy/' + self.user_journey + '/' + self.request_type + '/' + page + \
                       '/" lang="cy" >Cymraeg</a>'
        return link

    def check_text_enter_address(self, display_region, contents, check_empty=False, check_error=False):
        if display_region == 'cy':
            if self.user_journey == 'start':
                self.assertIn(self.content_start_exit_button_cy, contents)
            else:
                self.assertNotIn(self.content_start_exit_button_cy, contents)
            if check_empty:
                self.assertIn(self.content_request_enter_address_page_title_error_cy, contents)
                self.assertIn(self.content_common_enter_address_error_empty_cy, contents)
            elif check_error:
                self.assertIn(self.content_request_enter_address_page_title_error_cy, contents)
                self.assertIn(self.content_common_enter_address_error_cy, contents)
            else:
                self.assertIn(self.content_request_enter_address_page_title_cy, contents)
            self.assertIn(self.content_request_enter_address_title_cy, contents)
            self.assertIn(self.content_request_access_code_enter_address_secondary_cy, contents)
        else:
            if self.user_journey == 'start':
                self.assertIn(self.content_start_exit_button_en, contents)
            else:
                self.assertNotIn(self.content_start_exit_button_en, contents)
            if check_empty:
                self.assertIn(self.content_request_enter_address_page_title_error_en, contents)
                self.assertIn(self.content_common_enter_address_error_empty_en, contents)
            elif check_error:
                self.assertIn(self.content_request_enter_address_page_title_error_en, contents)
                self.assertIn(self.content_common_enter_address_error_en, contents)
            else:
                self.assertIn(self.content_request_enter_address_page_title_en, contents)
            self.assertIn(self.content_request_enter_address_title_en, contents)
            self.assertIn(self.content_request_access_code_enter_address_secondary_en, contents)

    def check_text_select_address(self, display_region, contents, check_error=False):
        if display_region == 'cy':
            if self.user_journey == 'start':
                self.assertIn(self.content_start_exit_button_cy, contents)
            else:
                self.assertNotIn(self.content_start_exit_button_cy, contents)
            if check_error:
                self.assertIn(self.content_common_select_address_error_cy, contents)
                self.assertIn(self.content_common_select_address_page_title_error_cy, contents)
            else:
                self.assertIn(self.content_common_select_address_page_title_cy, contents)
            self.assertIn(self.content_common_select_address_title_cy, contents)
            self.assertIn(self.content_common_select_address_value_cy, contents)
        else:
            if self.user_journey == 'start':
                self.assertIn(self.content_start_exit_button_en, contents)
            else:
                self.assertNotIn(self.content_start_exit_button_en, contents)
            if check_error:
                self.assertIn(self.content_common_select_address_error_en, contents)
                self.assertIn(self.content_common_select_address_page_title_error_en, contents)
            else:
                self.assertIn(self.content_common_select_address_page_title_en, contents)
            self.assertIn(self.content_common_select_address_title_en, contents)
            self.assertIn(self.content_common_select_address_value_en, contents)

    def check_text_confirm_address(self, display_region, contents, check_error=False):
        if display_region == 'cy':
            if self.user_journey == 'start':
                self.assertIn(self.content_start_exit_button_cy, contents)
            else:
                self.assertNotIn(self.content_start_exit_button_cy, contents)
            if check_error:
                self.assertIn(self.content_common_confirm_address_error_cy, contents)
                self.assertIn(self.content_common_confirm_address_page_title_error_cy, contents)
            else:
                self.assertIn(self.content_common_confirm_address_page_title_cy, contents)
            self.assertIn(self.content_common_confirm_address_title_cy, contents)
            self.assertIn(self.content_common_confirm_address_value_yes_cy, contents)
            self.assertIn(self.content_common_confirm_address_value_no_cy, contents)
        else:
            if self.user_journey == 'start':
                self.assertIn(self.content_start_exit_button_en, contents)
            else:
                self.assertNotIn(self.content_start_exit_button_en, contents)
            if check_error:
                self.assertIn(self.content_common_confirm_address_error_en, contents)
                self.assertIn(self.content_common_confirm_address_page_title_error_en, contents)
            else:
                self.assertIn(self.content_common_confirm_address_page_title_en, contents)
            self.assertIn(self.content_common_confirm_address_title_en, contents)
            self.assertIn(self.content_common_confirm_address_value_yes_en, contents)
            self.assertIn(self.content_common_confirm_address_value_no_en, contents)

    def check_text_select_how_to_receive(self, display_region, contents, check_error=False):
        if display_region == 'cy':
            if self.user_journey == 'start':
                self.assertIn(self.content_start_exit_button_cy, contents)
            else:
                self.assertNotIn(self.content_start_exit_button_cy, contents)
            if check_error:
                self.assertIn(self.content_request_code_select_how_to_receive_error_cy, contents)
            if check_error:
                self.assertIn(
                    self.content_request_code_select_how_to_receive_page_title_error_cy, contents)
            else:
                self.assertIn(self.content_request_code_select_how_to_receive_page_title_cy, contents)
            self.assertIn(self.content_request_code_select_how_to_receive_title_cy, contents)
            self.assertIn(self.content_request_code_select_how_to_receive_secondary_cy, contents)
            self.assertIn(self.content_request_code_select_how_to_receive_option_text_cy, contents)
            self.assertIn(self.content_request_code_select_how_to_receive_option_post_cy, contents)
            self.assertIn(self.content_request_code_select_how_to_receive_option_post_hint_cy, contents)
        else:
            if self.user_journey == 'start':
                self.assertIn(self.content_start_exit_button_en, contents)
            else:
                self.assertNotIn(self.content_start_exit_button_en, contents)
            if check_error:
                self.assertIn(self.content_request_code_select_how_to_receive_error_en, contents)
            if check_error:
                self.assertIn(
                    self.content_request_code_select_how_to_receive_page_title_error_en, contents)
            else:
                self.assertIn(self.content_request_code_select_how_to_receive_page_title_en, contents)
            self.assertIn(self.content_request_code_select_how_to_receive_title_en, contents)
            self.assertIn(self.content_request_code_select_how_to_receive_secondary_en, contents)
            self.assertIn(self.content_request_code_select_how_to_receive_option_text_en, contents)
            self.assertIn(self.content_request_code_select_how_to_receive_option_post_en, contents)
            self.assertIn(self.content_request_code_select_how_to_receive_option_post_hint_en, contents)

    def check_text_enter_mobile(self, display_region, contents, check_empty=False, check_error=False):
        if display_region == 'cy':
            if self.user_journey == 'start':
                self.assertIn(self.content_start_exit_button_cy, contents)
            else:
                self.assertNotIn(self.content_start_exit_button_cy, contents)
            if check_empty:
                self.assertIn(self.content_request_code_enter_mobile_error_empty_cy, contents)
            elif check_error:
                self.assertIn(self.content_request_code_enter_mobile_error_invalid_cy, contents)
            if check_empty or check_error:
                self.assertIn(self.content_request_code_enter_mobile_page_title_error_cy, contents)
            else:
                self.assertIn(self.content_request_code_enter_mobile_page_title_cy, contents)
            self.assertIn(self.content_request_code_enter_mobile_title_cy, contents)
            self.assertIn(self.content_request_code_enter_mobile_secondary_cy, contents)
        else:
            if self.user_journey == 'start':
                self.assertIn(self.content_start_exit_button_en, contents)
            else:
                self.assertNotIn(self.content_start_exit_button_en, contents)
            if check_empty:
                self.assertIn(self.content_request_code_enter_mobile_error_empty_en, contents)
            elif check_error:
                self.assertIn(self.content_request_code_enter_mobile_error_invalid_en, contents)
            if check_empty or check_error:
                self.assertIn(self.content_request_code_enter_mobile_page_title_error_en, contents)
            else:
                self.assertIn(self.content_request_code_enter_mobile_page_title_en, contents)
            self.assertIn(self.content_request_code_enter_mobile_title_en, contents)
            self.assertIn(self.content_request_code_enter_mobile_secondary_en, contents)

    def check_text_confirm_send_by_text(self, display_region, contents, check_error=False):
        if display_region == 'cy':
            if self.user_journey == 'start':
                self.assertIn(self.content_start_exit_button_cy, contents)
            else:
                self.assertNotIn(self.content_start_exit_button_cy, contents)
            if check_error:
                self.assertIn(self.content_request_code_confirm_send_by_text_error_cy, contents)
            if check_error:
                self.assertIn(self.content_request_code_confirm_send_by_text_page_title_error_cy,
                              contents)
            else:
                self.assertIn(self.content_request_code_confirm_send_by_text_page_title_cy, contents)
            self.assertIn(self.content_request_code_confirm_send_by_text_title_cy, contents)
        else:
            if self.user_journey == 'start':
                self.assertIn(self.content_start_exit_button_en, contents)
            else:
                self.assertNotIn(self.content_start_exit_button_en, contents)
            if check_error:
                self.assertIn(self.content_request_code_confirm_send_by_text_error_en, contents)
            if check_error:
                self.assertIn(self.content_request_code_confirm_send_by_text_page_title_error_en,
                              contents)
            else:
                self.assertIn(self.content_request_code_confirm_send_by_text_page_title_en, contents)
            self.assertIn(self.content_request_code_confirm_send_by_text_title_en, contents)

    def check_text_confirm_send_by_post(self, display_region, contents, check_error=False):
        if display_region == 'cy':
            if self.user_journey == 'start':
                self.assertIn(self.content_start_exit_button_cy, contents)
            else:
                self.assertNotIn(self.content_start_exit_button_cy, contents)
            if check_error:
                self.assertIn(self.content_request_common_confirm_send_by_post_error_cy, contents)
            if check_error:
                self.assertIn(self.content_request_code_confirm_send_by_post_page_title_error_cy,
                              contents)
            else:
                self.assertIn(self.content_request_code_confirm_send_by_post_page_title_cy, contents)
            self.assertIn(self.content_request_code_confirm_send_by_post_title_cy, contents)

            self.assertIn(self.content_request_code_confirm_send_by_post_option_yes_cy, contents)
            self.assertIn(self.content_request_code_confirm_send_by_post_option_no_cy, contents)
        else:
            if self.user_journey == 'start':
                self.assertIn(self.content_start_exit_button_en, contents)
            else:
                self.assertNotIn(self.content_start_exit_button_en, contents)
            if check_error:
                self.assertIn(self.content_request_common_confirm_send_by_post_error_en, contents)
            if check_error:
                self.assertIn(self.content_request_code_confirm_send_by_post_page_title_error_en,
                              contents)
            else:
                self.assertIn(self.content_request_code_confirm_send_by_post_page_title_en, contents)
            self.assertIn(self.content_request_code_confirm_send_by_post_title_en, contents)

            self.assertIn(self.content_request_code_confirm_send_by_post_option_yes_en, contents)
            self.assertIn(self.content_request_code_confirm_send_by_post_option_no_en, contents)

    def check_text_error_500(self, display_region, contents):
        if display_region == 'cy':
            self.assertNotIn(self.content_start_exit_button_cy, contents)
            self.assertIn(self.content_common_500_error_cy, contents)
        else:
            self.assertNotIn(self.content_start_exit_button_en, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    async def check_get_enter_address(self, display_region):
        with self.assertLogs('respondent-home', 'INFO') as cm:
            response = await self.client.request('GET', self.get_url_from_class('RequestEnterAddress', 'get',
                                                                                display_region,
                                                                                request_type=self.request_type))
            self.assertLogEvent(cm, self.build_url_log_entry('enter-address', display_region, 'GET'))
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            self.assertIn(self.build_translation_link('enter-address', display_region), contents)
            self.check_text_enter_address(display_region, contents, check_empty=False, check_error=False)

    async def check_post_enter_address(self, display_region):
        with self.assertLogs('respondent-home', 'INFO') as cm, \
                mock.patch('app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            response = await self.client.request('POST',
                                                 self.get_url_from_class(
                                                     'RequestEnterAddress', 'post',
                                                     display_region, request_type=self.request_type),
                                                 data=self.common_postcode_input_valid)

            self.assertLogEvent(cm, self.build_url_log_entry('enter-address', display_region, 'POST'))
            self.assertLogEvent(cm, 'valid postcode')
            self.assertLogEvent(cm, self.build_url_log_entry('select-address', display_region, 'GET'))

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            self.assertIn(self.build_translation_link('select-address', display_region), contents)
            self.check_text_select_address(display_region, contents, check_error=False)

    async def check_post_enter_address_input_returns_no_results(self, display_region):
        with self.assertLogs('respondent-home', 'INFO') as cm, \
                mock.patch('app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_no_results

            response = await self.client.request('POST',
                                                 self.get_url_from_class(
                                                     'RequestEnterAddress', 'post',
                                                     display_region, request_type=self.request_type),
                                                 data=self.common_postcode_input_valid)

            self.assertLogEvent(cm, self.build_url_log_entry('enter-address', display_region, 'POST'))
            self.assertLogEvent(cm, 'valid postcode')
            self.assertLogEvent(cm, self.build_url_log_entry('select-address', display_region, 'GET'))

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            self.assertIn(self.build_translation_link('select-address', display_region), contents)
            if display_region == 'cy':
                self.assertIn(self.content_common_select_address_no_results_cy, contents)
            else:
                self.assertIn(self.content_common_select_address_no_results_en, contents)

    async def check_post_enter_address_input_empty(self, display_region):
        with self.assertLogs('respondent-home', 'INFO') as cm:
            response = await self.client.request('POST',
                                                 self.get_url_from_class(
                                                     'RequestEnterAddress', 'post',
                                                     display_region, request_type=self.request_type),
                                                 data=self.common_postcode_input_empty)

            self.assertLogEvent(cm, self.build_url_log_entry('enter-address', display_region, 'POST'))
            self.assertLogEvent(cm, 'invalid postcode')

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            self.assertIn(self.build_translation_link('enter-address', display_region), contents)
            self.check_text_enter_address(display_region, contents, check_empty=True, check_error=False)

    async def check_post_enter_address_input_invalid(self, display_region):
        with self.assertLogs('respondent-home', 'INFO') as cm:
            response = await self.client.request('POST',
                                                 self.get_url_from_class(
                                                     'RequestEnterAddress', 'post',
                                                     display_region, request_type=self.request_type),
                                                 data=self.common_postcode_input_invalid)

            self.assertLogEvent(cm, self.build_url_log_entry('enter-address', display_region, 'POST'))
            self.assertLogEvent(cm, 'invalid postcode')

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            self.assertIn(self.build_translation_link('enter-address', display_region), contents)
            self.check_text_enter_address(display_region, contents, check_empty=False, check_error=True)

    async def check_post_select_address_no_selection_made(self, display_region):
        with self.assertLogs('respondent-home', 'INFO') as cm, \
                mock.patch('app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            response = await self.client.request('POST',
                                                 self.get_url_from_class(
                                                     'RequestSelectAddress', 'post',
                                                     display_region, request_type=self.request_type),
                                                 data=self.common_form_data_empty)

            self.assertLogEvent(cm, self.build_url_log_entry('select-address', display_region, 'POST'))
            self.assertLogEvent(cm, 'no address selected')

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            self.assertIn(self.build_translation_link('select-address', display_region), contents)
            self.check_text_select_address(display_region, contents, check_error=True)

    async def check_post_select_address(self, display_region, region):
        with self.assertLogs('respondent-home', 'INFO') as cm, \
                mock.patch('app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.RHService.get_case_by_uprn') as mocked_get_case_by_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            if region == 'W':
                mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_hh_w
            else:
                mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_hh_e

            response = await self.client.request('POST',
                                                 self.get_url_from_class(
                                                     'RequestSelectAddress', 'post',
                                                     display_region, request_type=self.request_type),
                                                 data=self.common_select_address_input_valid)

            self.assertLogEvent(cm, self.build_url_log_entry('select-address', display_region, 'POST'))
            self.assertLogEvent(cm, self.build_url_log_entry('confirm-address', display_region, 'GET'))

            self.assertLogEvent(cm, 'case matching uprn found in RHSvc')

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            self.assertIn(self.build_translation_link('confirm-address', display_region), contents)
            self.check_text_confirm_address(display_region, contents, check_error=False)

    async def check_post_select_address_no_case(self, display_region):
        with self.assertLogs('respondent-home', 'INFO') as cm, aioresponses(
            passthrough=[str(self.server._root)]
        ) as mocked_get_case_by_uprn:

            mocked_get_case_by_uprn.get(self.rhsvc_cases_by_uprn_url + self.selected_uprn, status=404)

            response = await self.client.request('POST',
                                                 self.get_url_from_class(
                                                     'RequestSelectAddress', 'post',
                                                     display_region, request_type=self.request_type),
                                                 data=self.common_select_address_input_valid)

            self.assertLogEvent(cm, self.build_url_log_entry('select-address', display_region, 'POST'))
            self.assertLogEvent(cm, self.build_url_log_entry('confirm-address', display_region, 'GET'))
            self.assertLogEvent(cm, 'no case matching uprn in RHSvc - return customer contact centre page')
            self.assertLogEvent(cm, self.build_url_log_entry('address-not-required', display_region, 'GET'))

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            self.assertIn(self.build_translation_link('address-not-required', display_region), contents)
            if display_region == 'cy':
                self.assertIn(self.content_common_contact_centre_title_cy, contents)
            else:
                self.assertIn(self.content_common_contact_centre_title_en, contents)

    async def check_post_select_address_error_from_get_cases(self, display_region):
        with self.assertLogs('respondent-home', 'INFO') as cm, \
                aioresponses(passthrough=[str(self.server._root)]) as mocked_get_case_by_uprn:

            mocked_get_case_by_uprn.get(self.rhsvc_cases_by_uprn_url + self.selected_uprn, status=400)

            response = await self.client.request('POST',
                                                 self.get_url_from_class(
                                                     'RequestSelectAddress', 'post',
                                                     display_region, request_type=self.request_type),
                                                 data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, self.build_url_log_entry('select-address', display_region, 'POST'))
            self.assertLogEvent(cm, self.build_url_log_entry('confirm-address', display_region, 'GET'))
            self.assertLogEvent(cm, 'error response from RHSvc')
            self.assertLogEvent(cm, 'bad request', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            self.check_text_error_500(display_region, contents)

    async def check_post_select_address_address_not_found(self, display_region):
        with self.assertLogs('respondent-home', 'INFO') as cm:
            response = await self.client.request('POST',
                                                 self.get_url_from_class(
                                                     'RequestSelectAddress', 'post',
                                                     display_region, request_type=self.request_type),
                                                 data=self.common_select_address_input_not_listed)

            self.assertLogEvent(cm, self.build_url_log_entry('select-address', display_region, 'POST'))
            self.assertLogEvent(cm, self.build_url_log_entry('address-not-found', display_region, 'GET', True))
            self.assertEqual(response.status, 200)

            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            self.assertIn(self.build_translation_link('address-not-found', display_region, True), contents)
            if display_region == 'cy':
                self.assertIn(self.content_common_contact_centre_title_cy, contents)
                self.assertIn(self.content_call_centre_number_cy, contents)
            else:
                self.assertIn(self.content_common_contact_centre_title_en, contents)
                self.assertIn(self.content_call_centre_number_ew, contents)

    async def check_post_confirm_address_input_invalid(self, display_region):
        with self.assertLogs('respondent-home', 'INFO') as cm, \
                mock.patch('app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.RHService.get_case_by_uprn') as mocked_get_case_by_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_hh_e

            response = await self.client.request('POST',
                                                 self.get_url_from_class(
                                                     'RequestConfirmAddress', 'post',
                                                     display_region, request_type=self.request_type),
                                                 data=self.common_confirm_address_input_invalid)
            self.assertLogEvent(cm, self.build_url_log_entry('confirm-address', display_region, 'POST'))
            self.assertLogEvent(cm, "address confirmation error")
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            self.assertIn(self.build_translation_link('confirm-address', display_region), contents)
            self.check_text_confirm_address(display_region, contents, check_error=True)

    async def check_post_confirm_address_input_no_selection(self, display_region):
        with self.assertLogs('respondent-home', 'INFO') as cm, \
                mock.patch('app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.RHService.get_case_by_uprn') as mocked_get_case_by_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_hh_e

            response = await self.client.request('POST',
                                                 self.get_url_from_class(
                                                     'RequestConfirmAddress', 'post',
                                                     display_region, request_type=self.request_type),
                                                 data=self.common_form_data_empty)
            self.assertLogEvent(cm, self.build_url_log_entry('confirm-address', display_region, 'POST'))
            self.assertLogEvent(cm, "address confirmation error")
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            self.assertIn(self.build_translation_link('confirm-address', display_region), contents)
            self.check_text_confirm_address(display_region, contents, check_error=True)

    async def check_post_confirm_address_input_no(self, display_region):
        with self.assertLogs('respondent-home', 'INFO') as cm, \
                mock.patch('app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            response = await self.client.request('POST',
                                                 self.get_url_from_class(
                                                     'RequestConfirmAddress', 'post',
                                                     display_region, request_type=self.request_type),
                                                 data=self.common_confirm_address_input_no)
            self.assertLogEvent(cm, self.build_url_log_entry('confirm-address', display_region, 'POST'))
            self.assertLogEvent(cm, self.build_url_log_entry('enter-address', display_region, 'GET'))

            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            self.assertIn(self.build_translation_link('enter-address', display_region), contents)
            self.check_text_enter_address(display_region, contents, check_empty=False, check_error=False)

    async def check_post_confirm_address_input_yes_code(self, display_region):
        with self.assertLogs('respondent-home', 'INFO') as cm:

            response = await self.client.request('POST',
                                                 self.get_url_from_class(
                                                     'RequestConfirmAddress', 'post',
                                                     display_region, request_type=self.request_type),
                                                 data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, self.build_url_log_entry('confirm-address', display_region, 'POST'))
            self.assertLogEvent(cm, self.build_url_log_entry('select-how-to-receive', display_region, 'GET'))

            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            self.assertIn(self.build_translation_link('select-how-to-receive', display_region), contents)
            self.check_text_select_how_to_receive(display_region, contents)

    async def check_post_select_how_to_receive_input_sms(self, display_region):
        with self.assertLogs('respondent-home', 'INFO') as cm:

            response = await self.client.request('POST',
                                                 self.get_url_from_class(
                                                     'RequestCodeSelectHowToReceive', 'post',
                                                     display_region, request_type=self.request_type),
                                                 data=self.request_code_select_how_to_receive_data_sms)
            self.assertLogEvent(cm, self.build_url_log_entry('select-how-to-receive', display_region, 'POST'))
            self.assertLogEvent(cm, self.build_url_log_entry('enter-mobile', display_region, 'GET'))
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            self.assertIn(self.build_translation_link('enter-mobile', display_region), contents)
            self.check_text_enter_mobile(display_region, contents)

    async def check_post_select_how_to_receive_input_post(self, display_region):
        with self.assertLogs('respondent-home', 'INFO') as cm:

            response = await self.client.request('POST',
                                                 self.get_url_from_class(
                                                     'RequestCodeSelectHowToReceive', 'post',
                                                     display_region, request_type=self.request_type),
                                                 data=self.request_code_select_how_to_receive_data_post)
            self.assertLogEvent(cm, self.build_url_log_entry('select-how-to-receive', display_region, 'POST'))
            self.assertLogEvent(cm, self.build_url_log_entry('enter-name', display_region, 'GET'))
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            self.assertIn(self.build_translation_link('enter-name', display_region), contents)
            if display_region == 'cy':
                self.assertIn(self.content_request_common_enter_name_page_title_cy, contents)
                self.assertIn(self.content_request_common_enter_name_title_cy, contents)
            else:
                self.assertIn(self.content_request_common_enter_name_page_title_en, contents)
                self.assertIn(self.content_request_common_enter_name_title_en, contents)

    async def check_post_select_how_to_receive_input_invalid(self, display_region):
        with self.assertLogs('respondent-home', 'INFO') as cm:

            response = await self.client.request('POST',
                                                 self.get_url_from_class(
                                                     'RequestCodeSelectHowToReceive', 'post',
                                                     display_region, request_type=self.request_type),
                                                 data=self.request_code_select_how_to_receive_data_invalid)
            self.assertLogEvent(cm, self.build_url_log_entry('select-how-to-receive', display_region, 'POST'))
            self.assertLogEvent(cm, "request method selection error")
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            self.assertIn(self.build_translation_link('select-how-to-receive', display_region), contents)
            self.check_text_select_how_to_receive(display_region, contents, check_error=True)

    async def check_post_select_how_to_receive_input_no_selection(self, display_region):
        with self.assertLogs('respondent-home', 'INFO') as cm:

            response = await self.client.request('POST',
                                                 self.get_url_from_class(
                                                     'RequestCodeSelectHowToReceive', 'post',
                                                     display_region, request_type=self.request_type),
                                                 data=self.common_form_data_empty)
            self.assertLogEvent(cm, self.build_url_log_entry('select-how-to-receive', display_region, 'POST'))
            self.assertLogEvent(cm, "request method selection error")
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            self.assertIn(self.build_translation_link('select-how-to-receive', display_region), contents)
            self.check_text_select_how_to_receive(display_region, contents, check_error=True)

    async def check_post_enter_mobile(self, display_region):
        with self.assertLogs('respondent-home', 'INFO') as cm:

            response = await self.client.request('POST',
                                                 self.get_url_from_class(
                                                     'RequestCodeEnterMobile', 'post',
                                                     display_region, request_type=self.request_type),
                                                 data=self.request_code_enter_mobile_form_data_valid)
            self.assertLogEvent(cm, self.build_url_log_entry('enter-mobile', display_region, 'POST'))
            self.assertLogEvent(cm, self.build_url_log_entry('confirm-send-by-text', display_region, 'GET'))
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            self.assertIn(self.build_translation_link('confirm-send-by-text', display_region), contents)
            self.check_text_confirm_send_by_text(display_region, contents, check_error=False)

    async def check_post_enter_mobile_input_invalid(self, display_region):
        with self.assertLogs('respondent-home', 'INFO') as cm:

            response = await self.client.request('POST',
                                                 self.get_url_from_class(
                                                     'RequestCodeEnterMobile', 'post',
                                                     display_region, request_type=self.request_type),
                                                 data=self.request_code_enter_mobile_form_data_invalid)

            self.assertLogEvent(cm, self.build_url_log_entry('enter-mobile', display_region, 'POST'))

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            self.assertIn(self.build_translation_link('enter-mobile', display_region), contents)
            self.check_text_enter_mobile(display_region, contents, check_error=True)

    async def check_post_enter_mobile_input_empty(self, display_region):
        with self.assertLogs('respondent-home', 'INFO') as cm:

            response = await self.client.request('POST',
                                                 self.get_url_from_class(
                                                     'RequestCodeEnterMobile', 'post',
                                                     display_region, request_type=self.request_type),
                                                 data=self.request_code_enter_mobile_form_data_empty)

            self.assertLogEvent(cm, self.build_url_log_entry('enter-mobile', display_region, 'POST'))

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            self.assertIn(self.build_translation_link('enter-mobile', display_region), contents)
            self.check_text_enter_mobile(display_region, contents, check_empty=True)

    async def check_post_confirm_send_by_text(self, display_region, region):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment_sms'
        ) as mocked_request_fulfilment_sms:

            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi_sms
            mocked_request_fulfilment_sms.return_value = self.rhsvc_request_fulfilment_sms

            response = await self.client.request('POST',
                                                 self.get_url_from_class(
                                                     'RequestCodeConfirmSendByText', 'post',
                                                     display_region, request_type=self.request_type),
                                                 data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, self.build_url_log_entry('confirm-send-by-text', display_region, 'POST'))
            self.assertLogEvent(cm, "fulfilment query: region=" + region + ", individual=false")
            self.assertLogEvent(cm, self.build_url_log_entry('code-sent-by-text', display_region, 'GET'))

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            self.assertIn(self.build_translation_link('code-sent-by-text', display_region), contents)
            if display_region == 'cy':
                self.assertIn(self.content_request_code_sent_by_text_title_cy, contents)
                self.assertIn(self.content_request_code_sent_by_text_page_title_cy, contents)
                self.assertIn(self.content_request_code_sent_by_text_secondary_cy, contents)
            else:
                self.assertIn(self.content_request_code_sent_by_text_title_en, contents)
                self.assertIn(self.content_request_code_sent_by_text_page_title_en, contents)
                self.assertIn(self.content_request_code_sent_by_text_secondary_en, contents)

    async def check_post_confirm_send_by_text_error_from_get_fulfilment(self, display_region, region):
        with self.assertLogs('respondent-home', 'INFO') as cm, aioresponses(
            passthrough=[str(self.server._root)]
        ) as mocked_aioresponses:

            mocked_aioresponses.get(self.rhsvc_url_fulfilments +
                                    '?caseType=HH&region=' + region +
                                    '&deliveryChannel=SMS&productGroup=UAC&individual=false', status=400)

            response = await self.client.request('POST',
                                                 self.get_url_from_class(
                                                     'RequestCodeConfirmSendByText', 'post',
                                                     display_region, request_type=self.request_type),
                                                 data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, self.build_url_log_entry('confirm-send-by-text', display_region, 'POST'))
            self.assertLogEvent(cm, 'bad request', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            self.check_text_error_500(display_region, contents)

    async def check_post_confirm_send_by_text_input_no(self, display_region):
        with self.assertLogs('respondent-home', 'INFO') as cm:

            response = await self.client.request('POST',
                                                 self.get_url_from_class(
                                                     'RequestCodeConfirmSendByText', 'post',
                                                     display_region, request_type=self.request_type),
                                                 data=self.request_code_mobile_confirmation_data_no)
            self.assertLogEvent(cm, self.build_url_log_entry('confirm-send-by-text', display_region, 'POST'))
            self.assertLogEvent(cm, self.build_url_log_entry('enter-mobile', display_region, 'GET'))

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            self.assertIn(self.build_translation_link('enter-mobile', display_region), contents)
            self.check_text_enter_mobile(display_region, contents)

    async def check_post_confirm_send_by_text_error_from_request_fulfilment(self, display_region):
        with self.assertLogs('respondent-home', 'INFO') as cm, \
                mock.patch('app.utils.RHService.get_fulfilment') as mocked_get_fulfilment, \
                aioresponses(passthrough=[str(self.server._root)]) as mocked_aioresponses:

            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_single_sms
            mocked_aioresponses.post(self.rhsvc_cases_url +
                                     'dc4477d1-dd3f-4c69-b181-7ff725dc9fa4/fulfilments/sms', status=400)

            response = await self.client.request('POST',
                                                 self.get_url_from_class(
                                                     'RequestCodeConfirmSendByText', 'post',
                                                     display_region, request_type=self.request_type),
                                                 data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, self.build_url_log_entry('confirm-send-by-text', display_region, 'POST'))
            self.assertLogEvent(cm, 'bad request', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            self.check_text_error_500(display_region, contents)

    async def check_post_confirm_send_by_text_error_429_from_request_fulfilment(self, display_region):
        with self.assertLogs('respondent-home', 'INFO') as cm, \
                mock.patch('app.utils.RHService.get_fulfilment') as mocked_get_fulfilment, \
                aioresponses(passthrough=[str(self.server._root)]) as mocked_aioresponses:

            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_single_sms
            mocked_aioresponses.post(self.rhsvc_cases_url +
                                     'dc4477d1-dd3f-4c69-b181-7ff725dc9fa4/fulfilments/sms', status=429)

            response = await self.client.request('POST',
                                                 self.get_url_from_class(
                                                     'RequestCodeConfirmSendByText', 'post',
                                                     display_region, request_type=self.request_type),
                                                 data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, self.build_url_log_entry('confirm-send-by-text', display_region, 'POST'))
            self.assertLogEvent(cm, 'too many requests', status_code=429)
            self.assertLogEvent(cm, 'session invalidated')
            self.assertEqual(response.status, 429)
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            if display_region == 'cy':
                self.assertIn(self.content_common_429_error_uac_title_cy, contents)
            else:
                self.assertIn(self.content_common_429_error_uac_title_en, contents)

    async def check_post_confirm_send_by_text_input_invalid(self, display_region):
        with self.assertLogs('respondent-home', 'INFO') as cm:

            response = await self.client.request('POST',
                                                 self.get_url_from_class(
                                                     'RequestCodeConfirmSendByText', 'post',
                                                     display_region, request_type=self.request_type),
                                                 data=self.request_code_mobile_confirmation_data_invalid)
            self.assertLogEvent(cm, self.build_url_log_entry('confirm-send-by-text', display_region, 'POST'))

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            self.assertIn(self.build_translation_link('confirm-send-by-text', display_region), contents)
            self.check_text_confirm_send_by_text(display_region, contents, check_error=True)

    async def check_post_confirm_send_by_text_input_no_selection(self, display_region):
        with self.assertLogs('respondent-home', 'INFO') as cm:

            response = await self.client.request('POST',
                                                 self.get_url_from_class(
                                                     'RequestCodeConfirmSendByText', 'post',
                                                     display_region, request_type=self.request_type),
                                                 data=self.request_code_mobile_confirmation_data_empty)
            self.assertLogEvent(cm, self.build_url_log_entry('confirm-send-by-text', display_region, 'POST'))

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            self.assertIn(self.build_translation_link('confirm-send-by-text', display_region), contents)
            self.check_text_confirm_send_by_text(display_region, contents, check_error=True)

    async def check_post_enter_address_error_from_ai(self, get_url, post_url, display_region, status):
        with self.assertLogs('respondent-home', 'INFO') as cm, \
                aioresponses(passthrough=[str(self.server._root)]) as mocked:
            url = self.addressindexsvc_url + self.postcode_valid + '?limit=' + self.aims_postcode_limit
            mocked.get(url, status=status)

            await self.client.request('GET', get_url)
            response = await self.client.request('POST', post_url, data=self.common_postcode_input_valid)
            if status == 400:
                self.assertLogEvent(cm, 'bad request', status_code=status)
            elif status == 429:
                self.assertLogEvent(cm, 'error in AIMS response', status_code=status)
            else:
                self.assertLogEvent(cm, 'error in response', status_code=status)
            self.assertLogEvent(cm, 'response error', status=status, method="get", url=url.replace(' ', '%20'))
            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            self.check_text_error_500(display_region, contents)

    def mock_ai_503s(self, mocked, times):
        for i in range(times):
            mocked.get(self.addressindexsvc_url + self.postcode_valid + '?limit=' + self.aims_postcode_limit,
                       status=503)

    async def check_post_enter_address_error_503_from_ai(self, url, display_region):
        with self.assertLogs('respondent-home', 'INFO') as cm, \
                aioresponses(passthrough=[str(self.server._root)]) as mocked:
            self.mock_ai_503s(mocked, attempts_retry_limit)

            response = await self.client.request('POST', url, data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'error in response', status_code=503)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            self.check_text_error_500(display_region, contents)

    async def check_post_enter_address_connection_error_from_ai(self, url, display_region, epoch=None):
        with self.assertLogs('respondent-home', 'WARN') as cm, \
                aioresponses(passthrough=[str(self.server._root)]) as mocked:

            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       exception=ClientConnectionError('Failed'))
            if epoch:
                self.app['ADDRESS_INDEX_EPOCH'] = epoch
                param = self.address_index_epoch_param_test
            else:
                param = self.address_index_epoch_param

            response = await self.client.request('POST', url, data=self.common_postcode_input_valid)

            self.assertLogEvent(cm, 'client failed to connect', url=self.addressindexsvc_url +
                                self.postcode_valid + param)

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.get_logo(display_region), contents)
        self.check_text_error_500(display_region, contents)

    async def check_get_timeout(self, url, display_region):
        with self.assertLogs('respondent-home', 'INFO') as cm:

            response = await self.client.request('GET', url)
            self.assertLogEvent(cm, self.build_url_log_entry('timeout', display_region, 'GET'))
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            self.assertIn(self.build_translation_link('timeout', display_region), contents)
            if display_region == 'cy':
                self.assertIn(self.content_common_timeout_cy, contents)
                self.assertIn(self.content_request_timeout_error_cy, contents)
            else:
                self.assertIn(self.content_common_timeout_en, contents)
                self.assertIn(self.content_request_timeout_error_en, contents)

    async def check_post_enter_name(self, display_region, long_surname=False):
        with self.assertLogs('respondent-home', 'INFO') as cm:

            if long_surname:
                response = await self.client.request('POST',
                                                     self.get_url_from_class(
                                                         'RequestCommonEnterName', 'post',
                                                         display_region, request_type=self.request_type),
                                                     data=self.request_common_enter_name_form_data_long_surname)
            else:
                response = await self.client.request('POST',
                                                     self.get_url_from_class(
                                                         'RequestCommonEnterName', 'post',
                                                         display_region, request_type=self.request_type),
                                                     data=self.request_common_enter_name_form_data_valid)
            self.assertLogEvent(cm, self.build_url_log_entry('enter-name', display_region, 'POST'))
            self.assertLogEvent(cm, self.build_url_log_entry('confirm-send-by-post', display_region, 'GET'))

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)

            self.assertIn(self.build_translation_link('confirm-send-by-post', display_region), contents)
            self.check_text_confirm_send_by_post(display_region, contents, check_error=False)

    async def check_post_enter_name_inputs_error(self, display_region, data):
        with self.assertLogs('respondent-home', 'INFO') as cm:

            response = await self.client.request('POST',
                                                 self.get_url_from_class(
                                                     'RequestCommonEnterName', 'post',
                                                     display_region, request_type=self.request_type),
                                                 data=data)
            self.assertLogEvent(cm, self.build_url_log_entry('enter-name', display_region, 'POST'))
            if (data.get('name_first_name')) and (len(data.get('name_first_name').split()) > 0):
                first_name = data.get('name_first_name')
            else:
                first_name = ''
            if (data.get('name_last_name')) and (len(data.get('name_last_name').split()) > 0):
                last_name = data.get('name_last_name')
            else:
                last_name = ''
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            self.assertIn(self.build_translation_link('enter-name', display_region), contents)
            if display_region == 'cy':
                if (first_name == '') and (last_name == ''):
                    self.assertNotIn(self.content_common_enter_name_check_first, contents)
                    self.assertNotIn(self.content_common_enter_name_check_last, contents)
                    self.assertIn(self.content_request_common_enter_name_error_first_name_cy, contents)
                    self.assertIn(self.content_request_common_enter_name_error_last_name_cy, contents)
                else:
                    if first_name == '':
                        self.assertNotIn(self.content_common_enter_name_check_first, contents)
                        self.assertIn(self.content_common_enter_name_check_last, contents)
                        self.assertIn(self.content_request_common_enter_name_error_first_name_cy, contents)
                    elif len(first_name) > 35:
                        self.assertNotIn(self.content_common_enter_name_check_long_first, contents)
                        self.assertIn(self.content_common_enter_name_check_last, contents)
                        self.assertIn(self.content_request_common_enter_name_error_first_name_overlength_cy, contents)
                    if last_name == '':
                        self.assertIn(self.content_common_enter_name_check_first, contents)
                        self.assertNotIn(self.content_common_enter_name_check_last, contents)
                        self.assertIn(self.content_request_common_enter_name_error_last_name_cy, contents)
                    elif len(last_name) > 35:
                        self.assertIn(self.content_common_enter_name_check_first, contents)
                        self.assertNotIn(self.content_common_enter_name_check_long_last, contents)
                        self.assertIn(self.content_request_common_enter_name_error_last_name_overlength_cy, contents)
                self.assertIn(self.content_request_common_enter_name_page_title_error_cy, contents)
                self.assertIn(self.content_request_common_enter_name_title_cy, contents)
            else:
                if (first_name == '') and (last_name == ''):
                    self.assertNotIn(self.content_common_enter_name_check_first, contents)
                    self.assertNotIn(self.content_common_enter_name_check_last, contents)
                    self.assertIn(self.content_request_common_enter_name_error_first_name_en, contents)
                    self.assertIn(self.content_request_common_enter_name_error_last_name_en, contents)
                else:
                    if first_name == '':
                        self.assertNotIn(self.content_common_enter_name_check_first, contents)
                        self.assertIn(self.content_common_enter_name_check_last, contents)
                        self.assertIn(self.content_request_common_enter_name_error_first_name_en, contents)
                    elif len(first_name) > 35:
                        self.assertNotIn(self.content_common_enter_name_check_long_first, contents)
                        self.assertIn(self.content_common_enter_name_check_last, contents)
                        self.assertIn(self.content_request_common_enter_name_error_first_name_overlength_en, contents)
                    if last_name == '':
                        self.assertIn(self.content_common_enter_name_check_first, contents)
                        self.assertNotIn(self.content_common_enter_name_check_last, contents)
                        self.assertIn(self.content_request_common_enter_name_error_last_name_en, contents)
                    elif len(last_name) > 35:
                        self.assertIn(self.content_common_enter_name_check_first, contents)
                        self.assertNotIn(self.content_common_enter_name_check_long_last, contents)
                        self.assertIn(self.content_request_common_enter_name_error_last_name_overlength_en, contents)
                self.assertIn(self.content_request_common_enter_name_page_title_error_en, contents)
                self.assertIn(self.content_request_common_enter_name_title_en, contents)

    async def check_post_confirm_send_by_post_input_yes(self, display_region, region):
        with self.assertLogs('respondent-home', 'INFO') as cm, \
                mock.patch('app.utils.RHService.get_fulfilment') as mocked_get_fulfilment, \
                mock.patch('app.utils.RHService.request_fulfilment_post') as mocked_request_fulfilment_post:

            if display_region == 'cy':
                mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi_post
            else:
                mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_single_post
            mocked_request_fulfilment_post.return_value = self.rhsvc_request_fulfilment_post

            data = self.request_common_confirm_send_by_post_data_yes
            response = await self.client.request('POST',
                                                 self.get_url_from_class(
                                                     'RequestCommonConfirmSendByPost', 'post',
                                                     display_region, request_type=self.request_type),
                                                 data=data)
            self.assertLogEvent(cm, self.build_url_log_entry('confirm-send-by-post', display_region, 'POST'))
            self.assertLogEvent(cm, "fulfilment query: region=" + region + ", individual=false")
            self.assertLogEvent(cm, self.build_url_log_entry('code-sent-by-post', display_region, 'GET'))

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            self.assertIn(self.build_translation_link('code-sent-by-post', display_region), contents)
            if display_region == 'cy':
                self.assertIn(self.content_request_code_hh_sent_post_title_cy, contents)
                self.assertIn(self.content_request_code_sent_by_post_page_title_cy, contents)
                self.assertIn(self.content_request_code_sent_post_secondary_cy, contents)
            else:
                if region == 'W':
                    self.assertIn(self.content_request_code_hh_region_w_sent_post_title_en, contents)
                else:
                    self.assertIn(self.content_request_code_hh_region_e_sent_post_title_en, contents)
                self.assertIn(self.content_request_code_sent_by_post_page_title_en, contents)
                self.assertIn(self.content_request_code_sent_post_secondary_household_en, contents)

    async def check_post_confirm_send_by_post_input_no(self, display_region):
        with self.assertLogs('respondent-home', 'INFO') as cm:

            response = await self.client.request('POST',
                                                 self.get_url_from_class(
                                                     'RequestCommonConfirmSendByPost', 'post',
                                                     display_region, request_type=self.request_type),
                                                 data=self.request_common_confirm_send_by_post_data_no)
            self.assertLogEvent(cm, self.build_url_log_entry('confirm-send-by-post', display_region, 'POST'))
            self.assertLogEvent(cm, self.build_url_log_entry('enter-mobile', display_region, 'GET'))

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            self.assertIn(self.build_translation_link('enter-mobile', display_region), contents)
            self.check_text_enter_mobile(display_region, contents, check_empty=False, check_error=False)

    async def check_post_confirm_send_by_post_input_invalid_or_no_selection(self, display_region, data):
        with self.assertLogs('respondent-home', 'INFO') as cm:

            response = await self.client.request('POST',
                                                 self.get_url_from_class(
                                                     'RequestCommonConfirmSendByPost', 'post',
                                                     display_region, request_type=self.request_type),
                                                 data=data)
            self.assertLogEvent(cm, self.build_url_log_entry('confirm-send-by-post', display_region, 'POST'))

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            self.assertIn(self.build_translation_link('confirm-send-by-post', display_region), contents)
            self.check_text_confirm_send_by_post(display_region, contents, check_error=True)

    async def check_post_confirm_send_by_post_error_from_get_fulfilment(self, display_region, region):
        with self.assertLogs('respondent-home', 'INFO') as cm, aioresponses(
            passthrough=[str(self.server._root)]
        ) as mocked_aioresponses:

            mocked_aioresponses.get(self.rhsvc_url_fulfilments +
                                    '?caseType=HH&region=' + region +
                                    '&deliveryChannel=POST&productGroup=UAC&individual=false', status=400)

            response = await self.client.request('POST',
                                                 self.get_url_from_class(
                                                     'RequestCommonConfirmSendByPost', 'post',
                                                     display_region, request_type=self.request_type),
                                                 data=self.request_common_confirm_send_by_post_data_yes)
            self.assertLogEvent(cm, self.build_url_log_entry('confirm-send-by-post', display_region, 'POST'))
            self.assertLogEvent(cm, 'bad request', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            self.check_text_error_500(display_region, contents)

    async def check_post_confirm_send_by_post_error_from_request_fulfilment(self, display_region):
        with self.assertLogs('respondent-home', 'INFO') as cm, \
                mock.patch('app.utils.RHService.get_fulfilment') as mocked_get_fulfilment, \
                aioresponses(passthrough=[str(self.server._root)]) as mocked_aioresponses:

            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_single_post
            mocked_aioresponses.post(self.rhsvc_cases_url +
                                     'dc4477d1-dd3f-4c69-b181-7ff725dc9fa4/fulfilments/post', status=400)

            response = await self.client.request('POST',
                                                 self.get_url_from_class(
                                                     'RequestCommonConfirmSendByPost', 'post',
                                                     display_region, request_type=self.request_type),
                                                 data=self.request_common_confirm_send_by_post_data_yes)
            self.assertLogEvent(cm, self.build_url_log_entry('confirm-send-by-post', display_region, 'POST'))
            self.assertLogEvent(cm, 'bad request', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            self.check_text_error_500(display_region, contents)

    async def check_post_confirm_send_by_post_error_429_from_request_fulfilment_uac(self, display_region):
        with self.assertLogs('respondent-home', 'INFO') as cm, \
                mock.patch('app.utils.RHService.get_fulfilment') as mocked_get_fulfilment, \
                aioresponses(passthrough=[str(self.server._root)]) as mocked_aioresponses:

            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_single_post
            mocked_aioresponses.post(self.rhsvc_cases_url +
                                     'dc4477d1-dd3f-4c69-b181-7ff725dc9fa4/fulfilments/post', status=429)

            response = await self.client.request('POST',
                                                 self.get_url_from_class(
                                                     'RequestCommonConfirmSendByPost', 'post',
                                                     display_region, request_type=self.request_type),
                                                 data=self.request_common_confirm_send_by_post_data_yes)
            self.assertLogEvent(cm, self.build_url_log_entry('confirm-send-by-post', display_region, 'POST'))
            self.assertLogEvent(cm, 'too many requests', status_code=429)
            self.assertLogEvent(cm, 'session invalidated')
            self.assertEqual(response.status, 429)
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            if display_region == 'cy':
                self.assertIn(self.content_common_429_error_uac_title_cy, contents)
            else:
                self.assertIn(self.content_common_429_error_uac_title_en, contents)

    async def assert_start_page_correct(self, url, display_region):
        with self.assertLogs('respondent-home', 'INFO') as cm:
            response = await self.client.request('GET', url)
            self.assertLogEvent(cm, self.build_url_log_entry(self.request_type, display_region, 'GET',
                                                             include_request_type=False,
                                                             include_page=False))
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            self.assertIn(self.build_translation_link(self.request_type, display_region, include_request_type=False,
                                                      include_page=False), contents)
            if display_region == 'cy':
                self.assertIn(self.content_start_title_cy, contents)
                self.assertIn(self.content_start_uac_title_cy, contents)
            else:
                self.assertIn(self.content_start_title_en, contents)
                self.assertIn(self.content_start_uac_title_en, contents)
            self.assertEqual(contents.count('input--text'), 1)
            self.assertIn('type="submit"', contents)

    async def check_get_start(self, display_region):
        with self.assertLogs('respondent-home', 'INFO') as cm:
            response = await self.client.request('GET', self.get_url_from_class('Start', 'get', display_region))
            self.assertLogEvent(cm, self.build_url_log_entry('', display_region, 'GET', include_request_type=False,
                                                             include_page=False))
            self.assertEqual(200, response.status)
            contents = str(await response.content.read())
            self.assertIn(self.get_logo(display_region), contents)
            self.assertIn(self.build_translation_link('', display_region, include_request_type=False,
                                                      include_page=False), contents)
            if display_region == 'cy':
                self.assertIn(self.content_start_title_cy, contents)
                self.assertIn(self.content_start_uac_title_cy, contents)
            else:
                self.assertIn(self.content_start_title_en, contents)
                self.assertIn(self.content_start_uac_title_en, contents)
            self.assertEqual(contents.count('input--text'), 1)
            self.assertIn('type="submit"', contents)
