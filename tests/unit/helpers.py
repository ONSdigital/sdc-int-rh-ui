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

    def check_text_enter_address(self, display_region, contents, check_empty=False, check_error=False):
        if display_region == 'cy':
            title_tag = 'Enter address'  # TODO Add Translation
            h1_title = 'Beth yw eich cod post?'
            secondary_text = 'To request a new access code, we need your address'  # TODO Add Translation
            error_text_link = "Rhowch god post dilys yn y Deyrnas Unedig"
            error_text = "Nodwch god post dilys yn y Deyrnas Unedig"
            error_text_empty = "Rhowch god post"
        else:
            title_tag = 'Enter address'
            h1_title = 'What is your postcode?'
            secondary_text = 'To request a new access code, we need your address'
            error_text_link = 'Enter a valid UK postcode'
            error_text = error_text_link
            error_text_empty = 'Enter a postcode'

        if self.user_journey == 'start':
            self.assertExitButton(display_region, contents)
        else:
            self.assertNotExitButton(display_region, contents)

        if check_empty:
            self.assertCorrectHeadTitleTag(display_region, title_tag, contents, error=True)
            self.assertErrorMessageDisplayed(display_region, 'answer', error_text_empty, 'error_postcode_empty',
                                             error_text_empty, contents)
            self.assertIn(error_text_empty, contents)
        elif check_error:
            self.assertCorrectHeadTitleTag(display_region, title_tag, contents, error=True)
            self.assertErrorMessageDisplayed(display_region, 'answer', error_text_link, 'error_postcode_invalid',
                                             error_text, contents)
        else:
            self.assertCorrectHeadTitleTag(display_region, title_tag, contents, error=False)

        self.assertCorrectQuestionText(h1_title, contents)
        self.assertIn(secondary_text, contents)

    def check_content_select_address(self, display_region, contents, check_error=False):
        if display_region == 'cy':
            title_tag = 'Dewis cyfeiriad'
            h1_title = 'Dewiswch eich cyfeiriad'
            option_text = '1 Gate Reach'
            error_text_link = "Dewiswch gyfeiriad"
            error_text = error_text_link
        else:
            title_tag = 'Select address'
            h1_title = 'Select your address'
            option_text = '1 Gate Reach'
            error_text_link = 'Select an address'
            error_text = error_text_link

        if self.user_journey == 'start':
            self.assertExitButton(display_region, contents)
        else:
            self.assertNotExitButton(display_region, contents)

        self.assertSiteLogo(display_region, contents)
        self.assertCorrectTranslationLink(contents, display_region, self.user_journey,
                                          self.request_type, 'select-address')

        if check_error:
            self.assertCorrectHeadTitleTag(display_region, title_tag, contents, error=True)
            self.assertErrorMessageDisplayed(display_region, 'answer', error_text_link, 'error-no-address-selected',
                                             error_text, contents)
        else:
            self.assertCorrectHeadTitleTag(display_region, title_tag, contents, error=False)

        self.assertCorrectQuestionText(h1_title, contents)
        self.assertIn(option_text, contents)

    def check_content_confirm_address(self, display_region, contents, check_error=False):
        if display_region == 'cy':
            title_tag = 'Cadarnhau cyfeiriad'
            h1_title = "Ai dyma\\\'r cyfeiriad cywir?"
            option_yes_text = "Ie, dyma\\\'r cyfeiriad cywir"
            option_no_text = "Na, rwyf am chwilio am fy nghyfeiriad eto"
            error_text_link = "Dewiswch ateb"
            error_text = error_text_link
        else:
            title_tag = 'Confirm address'
            h1_title = 'Is this the correct address?'
            option_yes_text = 'Yes, this is the correct address'
            option_no_text = 'No, search for address again'
            error_text_link = 'Select an answer'
            error_text = error_text_link

        if self.user_journey == 'start':
            self.assertExitButton(display_region, contents)
        else:
            self.assertNotExitButton(display_region, contents)

        self.assertSiteLogo(display_region, contents)
        self.assertCorrectTranslationLink(contents, display_region, self.user_journey,
                                          self.request_type, 'confirm-address')

        if check_error:
            self.assertCorrectHeadTitleTag(display_region, title_tag, contents, error=True)
            self.assertErrorMessageDisplayed(display_region, 'answer', error_text_link, 'no-selection',
                                             error_text, contents)
        else:
            self.assertCorrectHeadTitleTag(display_region, title_tag, contents, error=False)

        self.assertCorrectQuestionText(h1_title, contents)
        self.assertIn(option_yes_text, contents)
        self.assertIn(option_no_text, contents)

    def check_content_select_how_to_receive(self, display_region, contents, check_error=False):
        if display_region == 'cy':
            title_tag = 'Select how to receive access code'  # TODO Add Translation
            h1_title = "How would you like to receive a new access code?"  # TODO Add Translation
            secondary_text = "Dewiswch sut i anfon y cod mynediad"
            option_text = "Neges destun"
            option_post = "Post"
            option_post_hint = "Dim ond i&#39;r cyfeiriad cofrestredig y gallwn anfon codau mynediad"
            error_text_link = "Dewiswch ateb"
            error_text = error_text_link
        else:
            title_tag = 'Select how to receive access code'
            h1_title = 'How would you like to receive a new access code?'
            secondary_text = 'Select how to send access code'
            option_text = 'Text message'
            option_post = 'Post'
            option_post_hint = 'We can only send access codes to the registered address'
            error_text_link = 'Select an answer'
            error_text = error_text_link

        self.assertNotExitButton(display_region, contents)
        self.assertSiteLogo(display_region, contents)
        self.assertCorrectTranslationLink(contents, display_region, self.user_journey,
                                          self.request_type, 'select-how-to-receive')

        if check_error:
            self.assertCorrectHeadTitleTag(display_region, title_tag, contents, error=True)
            self.assertErrorMessageDisplayed(display_region, 'answer', error_text_link, 'no-selection',
                                             error_text, contents)
        else:
            self.assertCorrectHeadTitleTag(display_region, title_tag, contents, error=False)

        self.assertCorrectQuestionText(h1_title, contents)
        self.assertIn(secondary_text, contents)
        self.assertIn(option_text, contents)
        self.assertIn(option_post, contents)
        self.assertIn(option_post_hint, contents)

    def check_content_enter_mobile(self, display_region, contents, check_empty=False, check_error=False):
        if display_region == 'cy':
            title_tag = 'Nodi rhif ff\\xc3\\xb4n symudol'
            h1_title = "Beth yw eich rhif ff\\xc3\\xb4n symudol?"
            secondary_text = "Ni chaiff y rhif ei storio a dim ond unwaith i anfon y cod mynediad y caiff ei ddefnyddio"
            error_text_link = "Rhowch rif ff\\xc3\\xb4n symudol yn y Deyrnas Unedig mewn fformat dilys, " \
                              "er enghraifft, 07700 900345 neu +44 7700 900345"
            error_text = error_text_link
            error_text_empty = "Rhowch eich rhif ff\\xc3\\xb4n symudol"
        else:
            title_tag = 'Enter mobile number'
            h1_title = 'What is your mobile number?'
            secondary_text = 'This will not be stored and only used once to send the access code'
            error_text_link = 'Enter a UK mobile number in a valid format, for example, 07700 900345 or +44 7700 900345'
            error_text = error_text_link
            error_text_empty = 'Enter your mobile number'

        self.assertNotExitButton(display_region, contents)
        self.assertSiteLogo(display_region, contents)
        self.assertCorrectTranslationLink(contents, display_region, self.user_journey,
                                          self.request_type, 'enter-mobile')

        if check_empty:
            self.assertCorrectHeadTitleTag(display_region, title_tag, contents, error=True)
            self.assertErrorMessageDisplayed(display_region, 'answer', error_text_empty, 'mobile_empty',
                                             error_text_empty, contents)
            self.assertIn(error_text_empty, contents)
        elif check_error:
            self.assertCorrectHeadTitleTag(display_region, title_tag, contents, error=True)
            self.assertErrorMessageDisplayed(display_region, 'answer', error_text_link, 'mobile_invalid',
                                             error_text, contents)
        else:
            self.assertCorrectHeadTitleTag(display_region, title_tag, contents, error=False)

        self.assertCorrectQuestionText(h1_title, contents)
        self.assertIn(secondary_text, contents)

    def check_content_confirm_send_by_text(self, display_region, contents, check_error=False):
        if display_region == 'cy':
            title_tag = 'Confirm to send access code by text'  # TODO Add Translation
            h1_title = "Ydy\\xe2\\x80\\x99r rhif ff\\xc3\\xb4n symudol hwn yn gywir?"
            option_yes_text = "Ydy, anfonwch y neges destun"
            option_no_text = "Nac ydy, mae angen i mi ei newid"
            error_text_link = "Dewiswch ateb"
            error_text = error_text_link
        else:
            title_tag = 'Confirm to send access code by text'
            h1_title = 'Is this mobile number correct?'
            option_yes_text = 'Yes, send the text'
            option_no_text = 'No, I need to change it'
            error_text_link = 'Select an answer'
            error_text = error_text_link

        self.assertNotExitButton(display_region, contents)
        self.assertSiteLogo(display_region, contents)
        self.assertCorrectTranslationLink(contents, display_region, self.user_journey,
                                          self.request_type, 'confirm-send-by-text')

        if check_error:
            self.assertCorrectHeadTitleTag(display_region, title_tag, contents, error=True)
            self.assertErrorMessageDisplayed(display_region, 'answer', error_text_link, 'no-selection',
                                             error_text, contents)
        else:
            self.assertCorrectHeadTitleTag(display_region, title_tag, contents, error=False)
        self.assertCorrectQuestionText(h1_title, contents)
        self.assertIn(option_yes_text, contents)
        self.assertIn(option_no_text, contents)

    def check_content_confirm_send_by_post(self, display_region, contents, check_error=False):
        if display_region == 'cy':
            title_tag = 'Confirm to send access code by post'  # TODO Add Translation
            h1_title = "Do you want to send a new access code to this address?"  # TODO Add Translation
            option_yes_text = "Ydw, anfonwch y cod mynediad drwy\\\'r post"
            option_no_text = "Nac ydw, anfonwch y cod mynediad drwy neges destun"
            error_text_link = "Dewiswch ateb"
            error_text = error_text_link
        else:
            title_tag = 'Confirm to send access code by post'
            h1_title = 'Do you want to send a new access code to this address?'
            option_yes_text = 'Yes, send the access code by post'
            option_no_text = 'No, send it by text message'
            error_text_link = 'Select an answer'
            error_text = error_text_link

        self.assertNotExitButton(display_region, contents)
        self.assertSiteLogo(display_region, contents)
        self.assertCorrectTranslationLink(contents, display_region, self.user_journey,
                                          self.request_type, 'confirm-send-by-post')

        if check_error:
            self.assertCorrectHeadTitleTag(display_region, title_tag, contents, error=True)
            self.assertErrorMessageDisplayed(display_region, 'answer', error_text_link, 'no-selection',
                                             error_text, contents)
        else:
            self.assertCorrectHeadTitleTag(display_region, title_tag, contents, error=False)
        self.assertCorrectQuestionText(h1_title, contents)
        self.assertIn(option_yes_text, contents)
        self.assertIn(option_no_text, contents)

    def check_content_enter_email(self, display_region, contents, check_empty=False, check_error=False):
        if display_region == 'cy':
            title_tag = 'Enter email address'
            h1_title = "What is your email address?"
            secondary_text = "Ni chaiff y rhif ei storio a dim ond unwaith i anfon y cod mynediad y caiff ei ddefnyddio"
            error_text_link = "Enter an email address in a valid format, for example, name@example.com"
            error_text = error_text_link
            error_text_empty = "Enter an email address"
        else:
            title_tag = 'Enter email address'
            h1_title = 'What is your email address?'
            secondary_text = 'This will not be stored and only used once to send the access code'
            error_text_link = 'Enter an email address in a valid format, for example, name@example.com'
            error_text = error_text_link
            error_text_empty = 'Enter an email address'

        self.assertNotExitButton(display_region, contents)
        self.assertSiteLogo(display_region, contents)
        self.assertCorrectTranslationLink(contents, display_region, self.user_journey,
                                          self.request_type, 'enter-email')

        if check_empty:
            self.assertCorrectHeadTitleTag(display_region, title_tag, contents, error=True)
            self.assertErrorMessageDisplayed(display_region, 'answer', error_text_empty, 'email_empty',
                                             error_text_empty, contents)
            self.assertIn(error_text_empty, contents)
        elif check_error:
            self.assertCorrectHeadTitleTag(display_region, title_tag, contents, error=True)
            self.assertErrorMessageDisplayed(display_region, 'answer', error_text_link, 'email_invalid',
                                             error_text, contents)
        else:
            self.assertCorrectHeadTitleTag(display_region, title_tag, contents, error=False)

        self.assertCorrectQuestionText(h1_title, contents)
        self.assertIn(secondary_text, contents)

    def check_content_confirm_send_by_email(self, display_region, contents, check_error=False):
        if display_region == 'cy':
            title_tag = 'Confirm to send access code by email'  # TODO Add Translation
            h1_title = "Is the email address test@testing.com correct?"  # TODO Add Translation
            option_yes_text = "Yes, send the email"  # TODO Add Translation
            option_no_text = "Nac ydy, mae angen i mi ei newid"
            error_text_link = "Dewiswch ateb"
            error_text = error_text_link
        else:
            title_tag = 'Confirm to send access code by email'
            h1_title = 'Is the email address test@testing.com correct?'
            option_yes_text = 'Yes, send the email'
            option_no_text = 'No, I need to change it'
            error_text_link = 'Select an answer'
            error_text = error_text_link

        self.assertNotExitButton(display_region, contents)
        self.assertSiteLogo(display_region, contents)
        self.assertCorrectTranslationLink(contents, display_region, self.user_journey,
                                          self.request_type, 'confirm-send-by-email')

        if check_error:
            self.assertCorrectHeadTitleTag(display_region, title_tag, contents, error=True)
            self.assertErrorMessageDisplayed(display_region, 'answer', error_text_link, 'no-selection',
                                             error_text, contents)
        else:
            self.assertCorrectHeadTitleTag(display_region, title_tag, contents, error=False)
        self.assertCorrectQuestionText(h1_title, contents)
        self.assertIn(option_yes_text, contents)
        self.assertIn(option_no_text, contents)

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
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.service_calls.rhsvc.RHSvc.get_cases_by_uprn') as mocked_get_case_by_uprn:
            if region == 'W':
                mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_hh_w
            else:
                mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_hh_e

            response = await self.client.request('POST',
                                                 self.get_url_from_class(
                                                     'RequestEnterAddress', 'post',
                                                     display_region, request_type=self.request_type),
                                                 data=self.common_address_finder_input)

            self.assertLogEvent(cm, self.build_url_log_entry('enter-address', display_region, 'POST'))
            self.assertLogEvent(cm, 'UPRN of selected address: ' + self.selected_uprn)
            self.assertLogEvent(cm, self.build_url_log_entry('confirm-address', display_region, 'GET'))
            self.assertLogEvent(cm, 'case matching uprn found in RHSvc')
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
                mock.patch('app.service_calls.aims.Aims.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.service_calls.rhsvc.RHSvc.get_cases_by_uprn') as mocked_get_case_by_uprn:
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
            self.check_content_confirm_address(display_region, str(await response.content.read()), check_error=False)

    async def check_post_select_address_no_case(self, display_region):
        with self.assertLogs('respondent-home', 'INFO') as cm, \
                mock.patch('app.service_calls.aims.Aims.get_ai_uprn') as mocked_get_ai_uprn, \
                aioresponses(passthrough=[str(self.server._root)]) as mocked_get_case_by_uprn:

            mocked_get_case_by_uprn.get(self.rhsvc_cases_by_uprn_url + self.selected_uprn, status=404)
            if display_region == 'cy':
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
            self.assertLogEvent(cm, 'no case matching uprn in RHSvc - using AIMS data')
            self.assertEqual(response.status, 200)
            self.check_content_confirm_address(display_region, str(await response.content.read()), check_error=False)

            confirm_response = await self.client.request('POST',
                                                         self.get_url_from_class(
                                                             'RequestConfirmAddress', 'post',
                                                             display_region, request_type=self.request_type),
                                                         data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, self.build_url_log_entry('confirm-address', display_region, 'POST'))
            self.assertLogEvent(cm, 'no case matching uprn in RHSvc - return customer contact centre page')
            self.assertLogEvent(cm, self.build_url_log_entry('address-not-required', display_region, 'GET'))

            self.assertEqual(confirm_response.status, 200)
            contents = str(await confirm_response.content.read())
            self.assertSiteLogo(display_region, contents)
            self.assertCorrectTranslationLink(contents, display_region, self.user_journey,
                                              self.request_type, 'address-not-required')
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
            self.assert500Error(response, display_region, str(await response.content.read()))

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

    async def check_post_confirm_address_input_invalid(self, display_region):
        with self.assertLogs('respondent-home', 'INFO') as cm, \
                mock.patch('app.service_calls.aims.Aims.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.service_calls.rhsvc.RHSvc.get_cases_by_uprn') as mocked_get_case_by_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_hh_e

            response = await self.client.request('POST',
                                                 self.get_url_from_class(
                                                     'RequestConfirmAddress', 'post',
                                                     display_region, request_type=self.request_type),
                                                 data=self.common_confirm_address_input_invalid)
            self.assertLogEvent(cm, self.build_url_log_entry('confirm-address', display_region, 'POST'))
            self.assertLogEvent(cm, "address confirmation error")
            self.check_content_confirm_address(display_region, str(await response.content.read()), check_error=True)

    async def check_post_confirm_address_input_no_selection(self, display_region):
        with self.assertLogs('respondent-home', 'INFO') as cm, \
                mock.patch('app.service_calls.aims.Aims.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.service_calls.rhsvc.RHSvc.get_cases_by_uprn') as mocked_get_case_by_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_hh_e

            response = await self.client.request('POST',
                                                 self.get_url_from_class(
                                                     'RequestConfirmAddress', 'post',
                                                     display_region, request_type=self.request_type),
                                                 data=self.common_form_data_empty)
            self.assertLogEvent(cm, self.build_url_log_entry('confirm-address', display_region, 'POST'))
            self.assertLogEvent(cm, "address confirmation error")
            self.check_content_confirm_address(display_region, str(await response.content.read()), check_error=True)

    async def check_post_confirm_address_input_no(self, display_region):
        with self.assertLogs('respondent-home', 'INFO') as cm, \
                mock.patch('app.service_calls.aims.Aims.get_ai_postcode') as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

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

    async def check_post_confirm_address_input_yes_code(self, display_region):
        with self.assertLogs('respondent-home', 'INFO') as cm, \
                mock.patch('app.service_calls.rhsvc.RHSvc.get_survey_details') as mocked_get_survey_details:
            mocked_get_survey_details.return_value = self.rhsvc_get_surveys

            response = await self.client.request('POST',
                                                 self.get_url_from_class(
                                                     'RequestConfirmAddress', 'post',
                                                     display_region, request_type=self.request_type),
                                                 data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, self.build_url_log_entry('confirm-address', display_region, 'POST'))
            self.assertLogEvent(cm, self.build_url_log_entry('select-how-to-receive', display_region, 'GET'))
            self.check_content_select_how_to_receive(display_region, str(await response.content.read()))

    async def check_post_confirm_address_input_yes_code_no_fulfilments(self, display_region):
        with self.assertLogs('respondent-home', 'INFO') as cm, \
                mock.patch('app.service_calls.rhsvc.RHSvc.get_survey_details') as mocked_get_survey_details:
            mocked_get_survey_details.return_value = self.rhsvc_get_surveys_no_fulfilments

            response = await self.client.request('POST',
                                                 self.get_url_from_class(
                                                     'RequestConfirmAddress', 'post',
                                                     display_region, request_type=self.request_type),
                                                 data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, self.build_url_log_entry('confirm-address', display_region, 'POST'))
            self.assertLogEvent(cm, self.build_url_log_entry('select-how-to-receive', display_region, 'GET'))
            self.assertLogEvent(cm, "survey query returned no appropriate fulfilments")
            self.assert500Error(response, display_region, str(await response.content.read()))

    async def check_post_select_how_to_receive_input_sms(self, display_region):
        with self.assertLogs('respondent-home', 'INFO') as cm:
            response = await self.client.request('POST',
                                                 self.get_url_from_class(
                                                     'RequestCodeSelectHowToReceive', 'post',
                                                     display_region, request_type=self.request_type),
                                                 data=self.request_code_select_how_to_receive_data_sms)
            self.assertLogEvent(cm, self.build_url_log_entry('select-how-to-receive', display_region, 'POST'))
            self.assertLogEvent(cm, self.build_url_log_entry('enter-mobile', display_region, 'GET'))
            self.check_content_enter_mobile(display_region, str(await response.content.read()))

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
            self.assertSiteLogo(display_region, contents)
            self.assertCorrectTranslationLink(contents, display_region, self.user_journey,
                                              self.request_type, 'enter-name')
            if display_region == 'cy':
                self.assertIn(self.content_request_common_enter_name_page_title_cy, contents)
                self.assertIn(self.content_request_common_enter_name_title_cy, contents)
            else:
                self.assertIn(self.content_request_common_enter_name_page_title_en, contents)
                self.assertIn(self.content_request_common_enter_name_title_en, contents)

    async def check_post_select_how_to_receive_input_email(self, display_region):
        with self.assertLogs('respondent-home', 'INFO') as cm:
            response = await self.client.request('POST',
                                                 self.get_url_from_class(
                                                     'RequestCodeSelectHowToReceive', 'post',
                                                     display_region, request_type=self.request_type),
                                                 data=self.request_code_select_how_to_receive_data_email)
            self.assertLogEvent(cm, self.build_url_log_entry('select-how-to-receive', display_region, 'POST'))
            self.assertLogEvent(cm, self.build_url_log_entry('enter-email', display_region, 'GET'))
            self.check_content_enter_email(display_region, str(await response.content.read()))

    async def check_post_select_how_to_receive_input_invalid(self, display_region):
        with self.assertLogs('respondent-home', 'INFO') as cm, \
                mock.patch('app.service_calls.rhsvc.RHSvc.get_survey_details') as mocked_get_survey_details:
            mocked_get_survey_details.return_value = self.rhsvc_get_surveys

            response = await self.client.request('POST',
                                                 self.get_url_from_class(
                                                     'RequestCodeSelectHowToReceive', 'post',
                                                     display_region, request_type=self.request_type),
                                                 data=self.request_code_select_how_to_receive_data_invalid)
            self.assertLogEvent(cm, self.build_url_log_entry('select-how-to-receive', display_region, 'POST'))
            self.assertLogEvent(cm, "request method selection error")
            self.check_content_select_how_to_receive(display_region, str(await response.content.read()),
                                                     check_error=True)

    async def check_post_select_how_to_receive_input_no_selection(self, display_region):
        with self.assertLogs('respondent-home', 'INFO') as cm, \
                mock.patch('app.service_calls.rhsvc.RHSvc.get_survey_details') as mocked_get_survey_details:
            mocked_get_survey_details.return_value = self.rhsvc_get_surveys

            response = await self.client.request('POST',
                                                 self.get_url_from_class(
                                                     'RequestCodeSelectHowToReceive', 'post',
                                                     display_region, request_type=self.request_type),
                                                 data=self.common_form_data_empty)
            self.assertLogEvent(cm, self.build_url_log_entry('select-how-to-receive', display_region, 'POST'))
            self.assertLogEvent(cm, "request method selection error")
            self.check_content_select_how_to_receive(display_region, str(await response.content.read()),
                                                     check_error=True)

    async def check_post_enter_mobile(self, display_region):
        with self.assertLogs('respondent-home', 'INFO') as cm:
            response = await self.client.request('POST',
                                                 self.get_url_from_class(
                                                     'RequestCodeEnterMobile', 'post',
                                                     display_region, request_type=self.request_type),
                                                 data=self.request_code_enter_mobile_form_data_valid)
            self.assertLogEvent(cm, self.build_url_log_entry('enter-mobile', display_region, 'POST'))
            self.assertLogEvent(cm, self.build_url_log_entry('confirm-send-by-text', display_region, 'GET'))
            self.check_content_confirm_send_by_text(display_region, str(await response.content.read()),
                                                    check_error=False)

    async def check_post_enter_mobile_input_invalid(self, display_region):
        with self.assertLogs('respondent-home', 'INFO') as cm:
            response = await self.client.request('POST',
                                                 self.get_url_from_class(
                                                     'RequestCodeEnterMobile', 'post',
                                                     display_region, request_type=self.request_type),
                                                 data=self.request_code_enter_mobile_form_data_invalid)

            self.assertLogEvent(cm, self.build_url_log_entry('enter-mobile', display_region, 'POST'))

            self.assertEqual(response.status, 200)
            self.check_content_enter_mobile(display_region, str(await response.content.read()), check_error=True)

    async def check_post_enter_mobile_input_empty(self, display_region):
        with self.assertLogs('respondent-home', 'INFO') as cm:
            response = await self.client.request('POST',
                                                 self.get_url_from_class(
                                                     'RequestCodeEnterMobile', 'post',
                                                     display_region, request_type=self.request_type),
                                                 data=self.request_code_enter_mobile_form_data_empty)

            self.assertLogEvent(cm, self.build_url_log_entry('enter-mobile', display_region, 'POST'))

            self.assertEqual(response.status, 200)
            self.check_content_enter_mobile(display_region, str(await response.content.read()), check_empty=True)

    async def check_post_enter_email(self, display_region):
        with self.assertLogs('respondent-home', 'INFO') as cm:
            response = await self.client.request('POST',
                                                 self.get_url_from_class(
                                                     'RequestCodeEnterEmail', 'post',
                                                     display_region, request_type=self.request_type),
                                                 data=self.request_code_enter_email_form_data_valid)
            self.assertLogEvent(cm, self.build_url_log_entry('enter-email', display_region, 'POST'))
            self.assertLogEvent(cm, self.build_url_log_entry('confirm-send-by-email', display_region, 'GET'))
            self.check_content_confirm_send_by_email(display_region, str(await response.content.read()),
                                                     check_error=False)

    async def check_post_enter_email_input_invalid(self, display_region):
        with self.assertLogs('respondent-home', 'INFO') as cm:
            response = await self.client.request('POST',
                                                 self.get_url_from_class(
                                                     'RequestCodeEnterEmail', 'post',
                                                     display_region, request_type=self.request_type),
                                                 data=self.request_code_enter_email_form_data_invalid)

            self.assertLogEvent(cm, self.build_url_log_entry('enter-email', display_region, 'POST'))

            self.assertEqual(response.status, 200)
            self.check_content_enter_email(display_region, str(await response.content.read()), check_error=True)

    async def check_post_enter_email_input_empty(self, display_region):
        with self.assertLogs('respondent-home', 'INFO') as cm:
            response = await self.client.request('POST',
                                                 self.get_url_from_class(
                                                     'RequestCodeEnterEmail', 'post',
                                                     display_region, request_type=self.request_type),
                                                 data=self.request_code_enter_email_form_data_empty)

            self.assertLogEvent(cm, self.build_url_log_entry('enter-email', display_region, 'POST'))

            self.assertEqual(response.status, 200)
            self.check_content_enter_email(display_region, str(await response.content.read()), check_empty=True)

    async def check_post_confirm_send_by_text(self, display_region, region):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.service_calls.rhsvc.RHSvc.get_survey_details'
        ) as mocked_get_survey_details, mock.patch(
            'app.service_calls.rhsvc.RHSvc.request_fulfilment_sms'
        ) as mocked_request_fulfilment_sms:

            mocked_get_survey_details.return_value = self.rhsvc_get_surveys
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
            self.assertSiteLogo(display_region, contents)
            self.assertCorrectTranslationLink(contents, display_region, self.user_journey,
                                              self.request_type, 'code-sent-by-text')
            if display_region == 'cy':
                self.assertCorrectHeadTitleTag(display_region, 'Access code has been sent by text', contents,
                                               error=False)  # TODO Add translation
                self.assertCorrectPageTitle('Mae neges destun wedi cael ei hanfon i 07012345678 ', contents)
                self.assertIn('The text message with a new access code should arrive soon for you to start your study',
                              contents)  # TODO Add translation
            else:
                self.assertCorrectHeadTitleTag(display_region, 'Access code has been sent by text', contents,
                                               error=False)
                self.assertCorrectPageTitle('A text has been sent to 07012345678 ', contents)
                self.assertIn('The text message with a new access code should arrive soon for you to start your study',
                              contents)

    async def check_post_confirm_send_by_text_error_from_get_survey_details(self, display_region):
        with self.assertLogs('respondent-home', 'INFO') as cm, aioresponses(
                passthrough=[str(self.server._root)]
        ) as mocked_aioresponses:
            mocked_aioresponses.get(self.rhsvc_url_surveys + '/4a6c6e0a-6384-4da8-8c3c-7c56a801f792', status=400)

            response = await self.client.request('POST',
                                                 self.get_url_from_class(
                                                     'RequestCodeConfirmSendByText', 'post',
                                                     display_region, request_type=self.request_type),
                                                 data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, self.build_url_log_entry('confirm-send-by-text', display_region, 'POST'))
            self.assertLogEvent(cm, 'bad request', status_code=400)
            self.assert500Error(response, display_region, str(await response.content.read()))

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
            self.check_content_enter_mobile(display_region, str(await response.content.read()))

    async def check_post_confirm_send_by_text_error_from_request_fulfilment(self, display_region):
        with self.assertLogs('respondent-home', 'INFO') as cm, \
                mock.patch('app.service_calls.rhsvc.RHSvc.get_survey_details') as mocked_get_survey_details, \
                aioresponses(passthrough=[str(self.server._root)]) as mocked_aioresponses:
            mocked_get_survey_details.return_value = self.rhsvc_get_surveys
            mocked_aioresponses.post(self.rhsvc_cases_url +
                                     'dc4477d1-dd3f-4c69-b181-7ff725dc9fa4/fulfilments/sms', status=400)

            response = await self.client.request('POST',
                                                 self.get_url_from_class(
                                                     'RequestCodeConfirmSendByText', 'post',
                                                     display_region, request_type=self.request_type),
                                                 data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, self.build_url_log_entry('confirm-send-by-text', display_region, 'POST'))
            self.assertLogEvent(cm, 'bad request', status_code=400)
            self.assert500Error(response, display_region, str(await response.content.read()))

    async def check_post_confirm_send_by_text_error_429_from_request_fulfilment(self, display_region):
        with self.assertLogs('respondent-home', 'INFO') as cm, \
                mock.patch('app.service_calls.rhsvc.RHSvc.get_survey_details') as mocked_get_survey_details, \
                aioresponses(passthrough=[str(self.server._root)]) as mocked_aioresponses:

            mocked_get_survey_details.return_value = self.rhsvc_get_surveys
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
            self.assertSiteLogo(display_region, contents)
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
            self.check_content_confirm_send_by_text(display_region, str(await response.content.read()),
                                                    check_error=True)

    async def check_post_confirm_send_by_text_input_no_selection(self, display_region):
        with self.assertLogs('respondent-home', 'INFO') as cm:
            response = await self.client.request('POST',
                                                 self.get_url_from_class(
                                                     'RequestCodeConfirmSendByText', 'post',
                                                     display_region, request_type=self.request_type),
                                                 data=self.request_code_mobile_confirmation_data_empty)
            self.assertLogEvent(cm, self.build_url_log_entry('confirm-send-by-text', display_region, 'POST'))

            self.assertEqual(response.status, 200)
            self.check_content_confirm_send_by_text(display_region, str(await response.content.read()),
                                                    check_error=True)

    async def check_post_confirm_send_by_email(self, display_region, region):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.service_calls.rhsvc.RHSvc.get_survey_details'
        ) as mocked_get_survey_details, mock.patch(
            'app.service_calls.rhsvc.RHSvc.request_fulfilment_email'
        ) as mocked_request_fulfilment_email:

            mocked_get_survey_details.return_value = self.rhsvc_get_surveys
            mocked_request_fulfilment_email.return_value = self.rhsvc_request_fulfilment_email

            response = await self.client.request('POST',
                                                 self.get_url_from_class(
                                                     'RequestCodeConfirmSendByEmail', 'post',
                                                     display_region, request_type=self.request_type),
                                                 data=self.request_code_email_confirmation_data_yes)
            self.assertLogEvent(cm, self.build_url_log_entry('confirm-send-by-email', display_region, 'POST'))
            self.assertLogEvent(cm, "fulfilment query: region=" + region + ", individual=false")
            self.assertLogEvent(cm, self.build_url_log_entry('code-sent-by-email', display_region, 'GET'))

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertSiteLogo(display_region, contents)
            self.assertCorrectTranslationLink(contents, display_region, self.user_journey,
                                              self.request_type, 'code-sent-by-email')
            if display_region == 'cy':
                self.assertCorrectHeadTitleTag(display_region, 'Access code has been sent by email', contents,
                                               error=False)  # TODO Add translation
                self.assertCorrectPageTitle('An email has been sent to test@testing.com ', contents)
                self.assertIn('The email message with a new access code should arrive soon for you to start your study',
                              contents)  # TODO Add translation
            else:
                self.assertCorrectHeadTitleTag(display_region, 'Access code has been sent by email', contents,
                                               error=False)
                self.assertCorrectPageTitle('An email has been sent to test@testing.com ', contents)
                self.assertIn('The email message with a new access code should arrive soon for you to start your study',
                              contents)

    async def check_post_confirm_send_by_email_error_from_get_survey_details(self, display_region):
        with self.assertLogs('respondent-home', 'INFO') as cm, \
                aioresponses(passthrough=[str(self.server._root)]) as mocked_aioresponses:
            mocked_aioresponses.get(self.rhsvc_url_surveys + '/4a6c6e0a-6384-4da8-8c3c-7c56a801f792', status=400)

            response = await self.client.request('POST',
                                                 self.get_url_from_class(
                                                     'RequestCodeConfirmSendByEmail', 'post',
                                                     display_region, request_type=self.request_type),
                                                 data=self.request_code_email_confirmation_data_yes)
            self.assertLogEvent(cm, self.build_url_log_entry('confirm-send-by-email', display_region, 'POST'))
            self.assertLogEvent(cm, 'bad request', status_code=400)
            self.assert500Error(response, display_region, str(await response.content.read()))

    async def check_post_confirm_send_by_email_input_no(self, display_region):
        with self.assertLogs('respondent-home', 'INFO') as cm:
            response = await self.client.request('POST',
                                                 self.get_url_from_class(
                                                     'RequestCodeConfirmSendByEmail', 'post',
                                                     display_region, request_type=self.request_type),
                                                 data=self.request_code_email_confirmation_data_no)
            self.assertLogEvent(cm, self.build_url_log_entry('confirm-send-by-email', display_region, 'POST'))
            self.assertLogEvent(cm, self.build_url_log_entry('enter-email', display_region, 'GET'))

            self.assertEqual(response.status, 200)
            self.check_content_enter_email(display_region, str(await response.content.read()))

    async def check_post_confirm_send_by_email_error_from_request_fulfilment(self, display_region):
        with self.assertLogs('respondent-home', 'INFO') as cm, \
                mock.patch('app.service_calls.rhsvc.RHSvc.get_survey_details') as mocked_get_survey_details, \
                aioresponses(passthrough=[str(self.server._root)]) as mocked_aioresponses:
            mocked_get_survey_details.return_value = self.rhsvc_get_surveys
            mocked_aioresponses.post(self.rhsvc_cases_url +
                                     'dc4477d1-dd3f-4c69-b181-7ff725dc9fa4/fulfilments/email', status=400)

            response = await self.client.request('POST',
                                                 self.get_url_from_class(
                                                     'RequestCodeConfirmSendByEmail', 'post',
                                                     display_region, request_type=self.request_type),
                                                 data=self.request_code_email_confirmation_data_yes)
            self.assertLogEvent(cm, self.build_url_log_entry('confirm-send-by-email', display_region, 'POST'))
            self.assertLogEvent(cm, 'bad request', status_code=400)
            self.assert500Error(response, display_region, str(await response.content.read()))

    async def check_post_confirm_send_by_email_error_429_from_request_fulfilment(self, display_region):
        with self.assertLogs('respondent-home', 'INFO') as cm, \
                mock.patch('app.service_calls.rhsvc.RHSvc.get_survey_details') as mocked_get_survey_details, \
                aioresponses(passthrough=[str(self.server._root)]) as mocked_aioresponses:

            mocked_get_survey_details.return_value = self.rhsvc_get_surveys
            mocked_aioresponses.post(self.rhsvc_cases_url +
                                     'dc4477d1-dd3f-4c69-b181-7ff725dc9fa4/fulfilments/email', status=429)

            response = await self.client.request('POST',
                                                 self.get_url_from_class(
                                                     'RequestCodeConfirmSendByEmail', 'post',
                                                     display_region, request_type=self.request_type),
                                                 data=self.request_code_email_confirmation_data_yes)
            self.assertLogEvent(cm, self.build_url_log_entry('confirm-send-by-email', display_region, 'POST'))
            self.assertLogEvent(cm, 'too many requests', status_code=429)
            self.assertLogEvent(cm, 'session invalidated')
            self.assertEqual(response.status, 429)
            contents = str(await response.content.read())
            self.assertSiteLogo(display_region, contents)
            if display_region == 'cy':
                self.assertIn(self.content_common_429_error_uac_title_cy, contents)
            else:
                self.assertIn(self.content_common_429_error_uac_title_en, contents)

    async def check_post_confirm_send_by_email_input_invalid(self, display_region):
        with self.assertLogs('respondent-home', 'INFO') as cm:
            response = await self.client.request('POST',
                                                 self.get_url_from_class(
                                                     'RequestCodeConfirmSendByEmail', 'post',
                                                     display_region, request_type=self.request_type),
                                                 data=self.request_code_email_confirmation_data_invalid)
            self.assertLogEvent(cm, self.build_url_log_entry('confirm-send-by-email', display_region, 'POST'))

            self.assertEqual(response.status, 200)
            self.check_content_confirm_send_by_email(display_region, str(await response.content.read()),
                                                     check_error=True)

    async def check_post_confirm_send_by_email_input_no_selection(self, display_region):
        with self.assertLogs('respondent-home', 'INFO') as cm:
            response = await self.client.request('POST',
                                                 self.get_url_from_class(
                                                     'RequestCodeConfirmSendByEmail', 'post',
                                                     display_region, request_type=self.request_type),
                                                 data=self.request_code_email_confirmation_data_empty)
            self.assertLogEvent(cm, self.build_url_log_entry('confirm-send-by-email', display_region, 'POST'))

            self.assertEqual(response.status, 200)
            self.check_content_confirm_send_by_email(display_region, str(await response.content.read()),
                                                     check_error=True)

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
            self.assertSiteLogo(display_region, contents)
            self.assertCorrectTranslationLink(contents, display_region, self.user_journey,
                                              self.request_type, 'enter-name')
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
                mock.patch('app.service_calls.rhsvc.RHSvc.get_survey_details') as mocked_get_survey_details, \
                mock.patch('app.service_calls.rhsvc.RHSvc.request_fulfilment_post'
                           ) as mocked_request_fulfilment_post:

            mocked_get_survey_details.return_value = self.rhsvc_get_surveys
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
            self.assertSiteLogo(display_region, contents)
            self.assertCorrectTranslationLink(contents, display_region, self.user_journey,
                                              self.request_type, 'code-sent-by-post')
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
                self.assertIn(self.content_request_code_sent_post_secondary_en, contents)

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
            self.check_content_enter_mobile(display_region, str(await response.content.read()),
                                            check_empty=False, check_error=False)

    async def check_post_confirm_send_by_post_input_invalid_or_no_selection(self, display_region, data):
        with self.assertLogs('respondent-home', 'INFO') as cm:
            response = await self.client.request('POST',
                                                 self.get_url_from_class(
                                                     'RequestCommonConfirmSendByPost', 'post',
                                                     display_region, request_type=self.request_type),
                                                 data=data)
            self.assertLogEvent(cm, self.build_url_log_entry('confirm-send-by-post', display_region, 'POST'))

            self.assertEqual(response.status, 200)
            self.check_content_confirm_send_by_post(display_region, str(await response.content.read()),
                                                    check_error=True)

    async def check_post_confirm_send_by_post_error_from_get_survey_details(self, display_region):
        with self.assertLogs('respondent-home', 'INFO') as cm, aioresponses(
                passthrough=[str(self.server._root)]
        ) as mocked_aioresponses:
            mocked_aioresponses.get(self.rhsvc_url_surveys + '/4a6c6e0a-6384-4da8-8c3c-7c56a801f792', status=400)

            response = await self.client.request('POST',
                                                 self.get_url_from_class(
                                                     'RequestCommonConfirmSendByPost', 'post',
                                                     display_region, request_type=self.request_type),
                                                 data=self.request_common_confirm_send_by_post_data_yes)
            self.assertLogEvent(cm, self.build_url_log_entry('confirm-send-by-post', display_region, 'POST'))
            self.assertLogEvent(cm, 'bad request', status_code=400)
            self.assert500Error(response, display_region, str(await response.content.read()))

    async def check_post_confirm_send_by_post_error_from_request_fulfilment(self, display_region):
        with self.assertLogs('respondent-home', 'INFO') as cm, \
                mock.patch('app.service_calls.rhsvc.RHSvc.get_survey_details') as mocked_get_survey_details, \
                aioresponses(passthrough=[str(self.server._root)]) as mocked_aioresponses:
            mocked_get_survey_details.return_value = self.rhsvc_get_surveys
            mocked_aioresponses.post(self.rhsvc_cases_url +
                                     'dc4477d1-dd3f-4c69-b181-7ff725dc9fa4/fulfilments/post', status=400)

            response = await self.client.request('POST',
                                                 self.get_url_from_class(
                                                     'RequestCommonConfirmSendByPost', 'post',
                                                     display_region, request_type=self.request_type),
                                                 data=self.request_common_confirm_send_by_post_data_yes)
            self.assertLogEvent(cm, self.build_url_log_entry('confirm-send-by-post', display_region, 'POST'))
            self.assertLogEvent(cm, 'bad request', status_code=400)
            self.assert500Error(response, display_region, str(await response.content.read()))

    async def check_post_confirm_send_by_post_error_429_from_request_fulfilment_uac(self, display_region):
        with self.assertLogs('respondent-home', 'INFO') as cm, \
                mock.patch('app.service_calls.rhsvc.RHSvc.get_survey_details') as mocked_get_survey_details, \
                aioresponses(passthrough=[str(self.server._root)]) as mocked_aioresponses:

            mocked_get_survey_details.return_value = self.rhsvc_get_surveys
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
            self.assertSiteLogo(display_region, contents)
            if display_region == 'cy':
                self.assertIn(self.content_common_429_error_uac_title_cy, contents)
            else:
                self.assertIn(self.content_common_429_error_uac_title_en, contents)

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

    async def check_post_start_confirm_address_get_survey_launched_error(
            self, post_start_url, post_confirm_url, display_region, region, status):
        with self.assertLogs('respondent-home', 'INFO') as cm, \
                aioresponses(passthrough=[str(self.server._root)]) as mocked:
            if region == 'W':
                payload = self.uac_json_w
            else:
                payload = self.uac_json_e
            mocked.get(self.rhsvc_url, payload=payload)
            mocked.post(self.rhsvc_url_surveylaunched, status=status)

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
