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

    async def check_get_enter_address(self, display_region):
        with self.assertLogs('respondent-home', 'INFO') as cm:
            response = await self.client.request('GET', self.get_url_from_class('RequestEnterAddress', 'get',
                                                                                display_region,
                                                                                request_type=self.request_type))
            self.assertLogEvent(cm, self.build_url_log_entry('enter-address', display_region, 'GET'))
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertSiteLogo(display_region, contents)
            self.assertCorrectTranslationLink(contents, display_region, self.user_journey,
                                              self.request_type, 'enter-address')
            self.check_text_enter_address(display_region, contents, check_empty=False, check_error=False)

    async def check_post_enter_address(self, display_region):
        with self.assertLogs('respondent-home', 'INFO') as cm, \
                mock.patch('app.service_calls.aims.Aims.get_ai_postcode') as mocked_get_ai_postcode:
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
            self.check_content_select_address(display_region, str(await response.content.read()), check_error=False)

    async def check_post_enter_address_finder(self, display_region, region):
        with self.assertLogs('respondent-home', 'INFO') as cm,\
                mock.patch('app.service_calls.aims.Aims.get_ai_uprn') as mocked_get_ai_uprn:
            if region == 'W':
                mocked_get_ai_uprn.return_value = self.ai_uprn_result_wales
            else:
                mocked_get_ai_uprn.return_value = self.ai_uprn_result_england

            response = await self.client.request('POST',
                                                 self.get_url_from_class(
                                                     'RequestEnterAddress', 'post',
                                                     display_region, request_type=self.request_type),
                                                 data=self.common_address_finder_input)

            self.assertLogEvent(cm, self.build_url_log_entry('enter-address', display_region, 'POST'))
            self.assertLogEvent(cm, 'UPRN of selected address: ' + self.selected_uprn)
            self.assertLogEvent(cm, self.build_url_log_entry('confirm-address', display_region, 'GET'))
            self.assertEqual(response.status, 200)
            self.check_content_confirm_address(display_region, str(await response.content.read()), check_error=False)

    async def check_post_enter_address_input_returns_no_results(self, display_region):
        with self.assertLogs('respondent-home', 'INFO') as cm, \
                mock.patch('app.service_calls.aims.Aims.get_ai_postcode') as mocked_get_ai_postcode:
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
            self.assertSiteLogo(display_region, contents)
            self.assertCorrectTranslationLink(contents, display_region, self.user_journey,
                                              self.request_type, 'select-address')
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
            self.assertSiteLogo(display_region, contents)
            self.assertCorrectTranslationLink(contents, display_region, self.user_journey,
                                              self.request_type, 'enter-address')
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
            self.assertSiteLogo(display_region, contents)
            self.assertCorrectTranslationLink(contents, display_region, self.user_journey,
                                              self.request_type, 'enter-address')
            self.check_text_enter_address(display_region, contents, check_empty=False, check_error=True)

    async def check_post_select_address_no_selection_made(self, display_region):
        with self.assertLogs('respondent-home', 'INFO') as cm, \
                mock.patch('app.service_calls.aims.Aims.get_ai_postcode') as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            response = await self.client.request('POST',
                                                 self.get_url_from_class(
                                                     'RequestSelectAddress', 'post',
                                                     display_region, request_type=self.request_type),
                                                 data=self.common_form_data_empty)

            self.assertLogEvent(cm, self.build_url_log_entry('select-address', display_region, 'POST'))
            self.assertLogEvent(cm, 'no address selected')

            self.assertEqual(response.status, 200)
            self.check_content_select_address(display_region, str(await response.content.read()), check_error=True)

    async def check_post_select_address(self, display_region, region):
        with self.assertLogs('respondent-home', 'INFO') as cm, \
                mock.patch('app.service_calls.aims.Aims.get_ai_postcode') as mocked_get_ai_postcode, \
                mock.patch('app.service_calls.aims.Aims.get_ai_uprn') as mocked_get_ai_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            if region == 'W':
                mocked_get_ai_uprn.return_value = self.ai_uprn_result_wales
            else:
                mocked_get_ai_uprn.return_value = self.ai_uprn_result_england
            response = await self.client.request('POST',
                                                 self.get_url_from_class(
                                                     'RequestSelectAddress', 'post',
                                                     display_region, request_type=self.request_type),
                                                 data=self.common_select_address_input_valid)

            self.assertLogEvent(cm, self.build_url_log_entry('select-address', display_region, 'POST'))
            self.assertLogEvent(cm, self.build_url_log_entry('confirm-address', display_region, 'GET'))
            self.assertEqual(response.status, 200)
            self.check_content_confirm_address(display_region, str(await response.content.read()), check_error=False)

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
            self.assertSiteLogo(display_region, contents)
            self.assertCorrectTranslationLink(contents, display_region, self.user_journey,
                                              self.request_type, 'address-not-found')
            if display_region == 'cy':
                self.assertIn(self.content_common_contact_centre_title_cy, contents)
                self.assertIn(self.content_call_centre_number_cy, contents)
            else:
                self.assertIn(self.content_common_contact_centre_title_en, contents)
                self.assertIn(self.content_call_centre_number_ew, contents)

    async def check_post_confirm_address_input_invalid(self, display_region, region):
        with self.assertLogs('respondent-home', 'INFO') as cm, \
                mock.patch('app.service_calls.aims.Aims.get_ai_uprn') as mocked_get_ai_uprn:
            if region == 'W':
                mocked_get_ai_uprn.return_value = self.ai_uprn_result_wales
            else:
                mocked_get_ai_uprn.return_value = self.ai_uprn_result_england

            response = await self.client.request('POST',
                                                 self.get_url_from_class(
                                                     'RequestConfirmAddress', 'post',
                                                     display_region, request_type=self.request_type),
                                                 data=self.common_confirm_address_input_invalid)
            self.assertLogEvent(cm, self.build_url_log_entry('confirm-address', display_region, 'POST'))
            self.assertLogEvent(cm, "address confirmation error")
            self.check_content_confirm_address(display_region, str(await response.content.read()), check_error=True)

    async def check_post_confirm_address_input_no_selection(self, display_region, region):
        with self.assertLogs('respondent-home', 'INFO') as cm, \
                mock.patch('app.service_calls.aims.Aims.get_ai_uprn') as mocked_get_ai_uprn:
            if region == 'W':
                mocked_get_ai_uprn.return_value = self.ai_uprn_result_wales
            else:
                mocked_get_ai_uprn.return_value = self.ai_uprn_result_england

            response = await self.client.request('POST',
                                                 self.get_url_from_class(
                                                     'RequestConfirmAddress', 'post',
                                                     display_region, request_type=self.request_type),
                                                 data=self.common_form_data_empty)
            self.assertLogEvent(cm, self.build_url_log_entry('confirm-address', display_region, 'POST'))
            self.assertLogEvent(cm, "address confirmation error")
            self.check_content_confirm_address(display_region, str(await response.content.read()), check_error=True)

    async def check_post_confirm_address_input_no(self, display_region, region):
        with self.assertLogs('respondent-home', 'INFO') as cm, \
                mock.patch('app.service_calls.aims.Aims.get_ai_uprn') as mocked_get_ai_uprn:
            if region == 'W':
                mocked_get_ai_uprn.return_value = self.ai_uprn_result_wales
            else:
                mocked_get_ai_uprn.return_value = self.ai_uprn_result_england

            response = await self.client.request('POST',
                                                 self.get_url_from_class(
                                                     'RequestConfirmAddress', 'post',
                                                     display_region, request_type=self.request_type),
                                                 data=self.common_confirm_address_input_no)
            self.assertLogEvent(cm, self.build_url_log_entry('confirm-address', display_region, 'POST'))
            self.assertLogEvent(cm, self.build_url_log_entry('enter-address', display_region, 'GET'))

            contents = str(await response.content.read())
            self.assertSiteLogo(display_region, contents)
            self.assertCorrectTranslationLink(contents, display_region, self.user_journey,
                                              self.request_type, 'enter-address')
            self.check_text_enter_address(display_region, contents, check_empty=False, check_error=False)

    async def check_post_confirm_address_input_yes_code(self, display_region, region):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.service_calls.rhsvc.RHSvc.get_cases_by_attribute') as mocked_get_cases_by_attribute, \
                mock.patch('app.service_calls.rhsvc.RHSvc.get_survey_details') as mocked_get_survey_details:
            mocked_get_survey_details.return_value = self.rhsvc_get_surveys
            if region == 'W':
                mocked_get_cases_by_attribute.return_value = self.rhsvc_case_by_attribute_uprn_single_w
            else:
                mocked_get_cases_by_attribute.return_value = self.rhsvc_case_by_attribute_uprn_single_e

            response = await self.client.request('POST',
                                                 self.get_url_from_class(
                                                     'RequestConfirmAddress', 'post',
                                                     display_region, request_type=self.request_type),
                                                 data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, self.build_url_log_entry('confirm-address', display_region, 'POST'))
            self.assertLogEvent(cm, self.build_url_log_entry('select-how-to-receive', display_region, 'GET'))
            self.check_content_select_how_to_receive(display_region, str(await response.content.read()))

    async def check_post_confirm_address_input_yes_no_cases(self, display_region):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.service_calls.rhsvc.RHSvc.get_cases_by_attribute') as mocked_get_cases_by_attribute:
            mocked_get_cases_by_attribute.return_value = self.rhsvc_empty_array

            response = await self.client.request('POST',
                                                 self.get_url_from_class(
                                                     'RequestConfirmAddress', 'post',
                                                     display_region, request_type=self.request_type),
                                                 data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, self.build_url_log_entry('confirm-address', display_region, 'POST'))
            self.assertLogEvent(cm, 'no case matching uprn in RHSvc - return customer contact centre page')
            self.assertLogEvent(cm, self.build_url_log_entry('address-not-required', display_region, 'GET'))
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertSiteLogo(display_region, contents)
            self.assertCorrectTranslationLink(contents, display_region, self.user_journey,
                                              self.request_type, 'address-not-required')
            if display_region == 'cy':
                self.assertIn(self.content_common_contact_centre_title_cy, contents)
            else:
                self.assertIn(self.content_common_contact_centre_title_en, contents)

    async def check_post_confirm_address_input_yes_multiple_cases(self, display_region, region):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.service_calls.rhsvc.RHSvc.get_cases_by_attribute') as mocked_get_cases_by_attribute:
            if region == 'W':
                mocked_get_cases_by_attribute.return_value = self.rhsvc_case_by_attribute_uprn_multiple_w
            else:
                mocked_get_cases_by_attribute.return_value = self.rhsvc_case_by_attribute_uprn_multiple_e

            response = await self.client.request('POST',
                                                 self.get_url_from_class(
                                                     'RequestConfirmAddress', 'post',
                                                     display_region, request_type=self.request_type),
                                                 data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, self.build_url_log_entry('confirm-address', display_region, 'POST'))
            self.assertLogEvent(cm, 'multiple cases matching uprn found in RHSvc - return customer contact centre page')
            self.assertLogEvent(cm, self.build_url_log_entry('multiple-cases', display_region, 'GET'))
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertSiteLogo(display_region, contents)
            self.assertCorrectTranslationLink(contents, display_region, self.user_journey,
                                              self.request_type, 'multiple-cases')
            if display_region == 'cy':
                self.assertIn(self.content_common_contact_centre_title_cy, contents)
            else:
                self.assertIn(self.content_common_contact_centre_title_en, contents)

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
            self.assert500Error(response, display_region, str(await response.content.read()))

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
            self.assert500Error(response, display_region, str(await response.content.read()))

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

            self.assertLogEvent(cm, 'client failed to connect',
                                url=self.addressindexsvc_url + self.postcode_valid + param)
        self.assert500Error(response, display_region, str(await response.content.read()))

    async def check_get_timeout(self, url, display_region):
        with self.assertLogs('respondent-home', 'INFO') as cm:

            response = await self.client.request('GET', url)
            self.assertLogEvent(cm, self.build_url_log_entry('timeout', display_region, 'GET'))
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertSiteLogo(display_region, contents)
            self.assertCorrectTranslationLink(contents, display_region, self.user_journey,
                                              self.request_type, 'timeout')
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
            self.check_content_confirm_send_by_post(display_region, str(await response.content.read()),
                                                    check_error=False)

    def check_content_start(self, display_region, contents, check_empty=False, check_error=False):
        if display_region == 'cy':
            title_tag = 'Start survey'  # TODO Add Translation
            h1_title = 'Start study'
            secondary_text = "Rhowch eich cod mynediad, sy\\\'n cynnwys 16 nod"
            error_text_link = "Rhowch god mynediad dilys"
            error_text = error_text_link
            error_text_empty = 'Rhowch god mynediad'
        else:
            title_tag = 'Start survey'
            h1_title = 'Start study'
            secondary_text = 'Enter your 16-character access code'
            error_text_link = 'Enter a valid access code'
            error_text = error_text_link
            error_text_empty = 'Enter an access code'

        self.assertNotExitButton(display_region, contents)
        self.assertSiteLogo(display_region, contents)
        self.assertCorrectTranslationLink(contents, display_region, self.user_journey)

        if check_empty:
            self.assertCorrectHeadTitleTag(display_region, title_tag, contents, error=True)
            self.assertErrorMessageDisplayed(display_region, 'page', error_text_empty, 'uac_invalid',
                                             error_text_empty, contents)
            self.assertIn(error_text_empty, contents)
        elif check_error:
            self.assertCorrectHeadTitleTag(display_region, title_tag, contents, error=True)
            self.assertErrorMessageDisplayed(display_region, 'page', error_text_link, 'uac_invalid',
                                             error_text, contents)
        else:
            self.assertCorrectHeadTitleTag(display_region, title_tag, contents, error=False)

        self.assertIn('<h1 class="ons-u-fs-xxl ons-u-mt-l">' + h1_title + '</h1>', contents)
        self.assertIn(secondary_text, contents)
        self.assertEqual(contents.count('input--text'), 1)
        self.assertIn('type="submit"', contents)

    async def check_get_start(self, display_region):
        with self.assertLogs('respondent-home', 'INFO') as cm:
            response = await self.client.request('GET', self.get_url_from_class('Start', 'get', display_region))
            self.assertLogEvent(cm, self.build_url_log_entry('', display_region, 'GET', include_request_type=False,
                                                             include_page=False))
            self.assertEqual(200, response.status)
            self.check_content_start(display_region, str(await response.content.read()))

    def get_launch_token_url_path(self, display_region):
        """ build the URL path for calling RHSvc to get the EQ token """
        base = self.rhsvc_url_get_launch_token
        p1 = 'languageCode=' + display_region
        p2 = 'accountServiceUrl=' + self.get_full_account_service_url(display_region)
        p3 = 'accountServiceLogoutUrl=' + self.get_full_account_service_logout_url(display_region)
        p4 = 'clientIP=None'
        url = f'{base}?{p1}&{p2}&{p3}&{p4}'
        return url

    async def check_post_start_confirm_address_get_survey_launched_error(
            self, post_start_url, post_confirm_url, display_region, region, status):
        with self.assertLogs('respondent-home', 'INFO') as cm, \
                aioresponses(passthrough=[str(self.server._root)]) as mocked:
            if region == 'W':
                payload = self.uac_json_w
            else:
                payload = self.uac_json_e
            mocked.get(self.rhsvc_url, payload=payload)
            mocked.get(self.get_launch_token_url_path(display_region), status=status)

            await self.client.request('POST', post_start_url, data=self.start_data_valid)
            response = await self.client.request(
                'POST', post_confirm_url, allow_redirects=False, data=self.start_confirm_address_data_yes)
            if status in [401, 500]:
                self.assertLogEvent(cm, 'error in response', status_code=status)
                self.assertEqual(response.status, 500)
            elif status == 429:
                self.assertLogEvent(cm, 'too many requests', status_code=429)
                self.assertLogEvent(cm, 'session invalidated')
                self.assertEqual(response.status, 429)

            contents = str(await response.content.read())
            self.assertSiteLogo(display_region, contents)
            if status == 429:
                self.assertNotExitButton(display_region, contents)
                if display_region == 'cy':
                    self.assertIn(self.content_common_429_error_eq_launch_title_cy, contents)
                else:
                    self.assertIn(self.content_common_429_error_eq_launch_title_en, contents)
            else:
                self.assert500Error(response, display_region, contents, check_exit=True)

    async def check_post_start_get_uac_error(self, post_start_url, display_region, status):
        with self.assertLogs('respondent-home', 'INFO') as cm, \
                aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, status=status)

            response = await self.client.request('POST', post_start_url, data=self.start_data_valid)
            if status == 400:
                self.assertLogEvent(cm, 'bad request', status_code=400)
            else:
                self.assertLogEvent(cm, 'error in response', status_code=status)
            self.assertLogEvent(cm, 'response error')
        self.assert500Error(response, display_region, str(await response.content.read()), check_exit=True)
