from aiohttp.test_utils import unittest_run_loop

from .helpers import TestHelpers


# noinspection PyTypeChecker
class TestWebFormHandlers(TestHelpers):
    user_journey = 'register'
    request_type = 'person'

    def check_content_register(self, display_region, contents):
        self.assertCorrectHeadTitleTag(display_region, 'Take part in a survey', contents, error=False)
        self.assertSiteLogo(display_region, contents)
        self.assertNotExitButton(display_region, contents)
        self.assertCorrectPageTitle('Take part in a survey', contents)
        self.assertIn('How to register a child', contents)

    def check_content_register_start(self, display_region, contents):
        self.assertCorrectHeadTitleTag(display_region, 'Start registration', contents, error=False)
        self.assertSiteLogo(display_region, contents)
        self.assertNotExitButton(display_region, contents)
        self.assertCorrectPageTitle('Register a child', contents)
        self.assertIn('Start', contents)

    def check_content_register_consent(self, display_region, contents):
        self.assertCorrectHeadTitleTag(display_region, 'Confirm consent', contents, error=False)
        self.assertSiteLogo(display_region, contents)
        self.assertNotExitButton(display_region, contents)
        self.assertCorrectPageTitle('Confirm consent', contents)
        self.assertIn('I accept', contents)
        self.assertIn('I decline', contents)

    def check_content_register_consent_declined(self, display_region, contents):
        self.assertCorrectHeadTitleTag(display_region, 'You have been removed from this study', contents, error=False)
        self.assertSiteLogo(display_region, contents)
        self.assertNotExitButton(display_region, contents)
        self.assertCorrectPageTitle('You have been removed from this study', contents)

    def check_content_register_enter_mobile(self, display_region, contents, error=None):
        title_tag = 'Enter mobile number'
        if error:
            if error == 'empty':
                error_text = 'Enter your mobile number'
                self.assertErrorMessageDisplayed(display_region, 'answer', error_text, 'mobile_empty',
                                                 error_text, contents)
            else:
                error_text = 'Enter a UK mobile number in a valid format, for example, 07700 900345 or +44 7700 900345'
                self.assertErrorMessageDisplayed(display_region, 'answer', error_text, 'mobile_invalid',
                                                 error_text, contents)
            self.assertCorrectHeadTitleTag(display_region, title_tag, contents, error=True)
            self.assertIn(error_text, contents)
        else:
            self.assertCorrectHeadTitleTag(display_region, title_tag, contents, error=False)
        self.assertSiteLogo(display_region, contents)
        self.assertNotExitButton(display_region, contents)
        self.assertCorrectQuestionText('What is your mobile number?', contents)
        self.assertIn('UK mobile number', contents)
        self.assertIn('This will be stored and used to send study access codes', contents)

    def check_content_register_confirm_registration(self, display_region, contents, error=None):
        title_tag = 'Confirm your registration'
        if error:
            error_text = 'Select an answer'
            self.assertCorrectHeadTitleTag(display_region, title_tag, contents, error=True)
            self.assertErrorMessageDisplayed(display_region, 'answer', error_text, 'no-selection',
                                             error_text, contents)
            self.assertIn(error_text, contents)
        else:
            self.assertCorrectHeadTitleTag(display_region, title_tag, contents, error=False)
        self.assertSiteLogo(display_region, contents)
        self.assertNotExitButton(display_region, contents)
        self.assertCorrectQuestionText('Is this mobile number correct?', contents)
        self.assertIn('Yes, process my registration', contents)
        self.assertIn('No, I need to change it', contents)

    def check_content_register_complete(self, display_region, contents):
        self.assertCorrectHeadTitleTag(display_region, 'Registration complete', contents, error=False)
        self.assertSiteLogo(display_region, contents)
        self.assertNotExitButton(display_region, contents)
        self.assertCorrectPageTitle('Your children have been registered for the survey', contents)
        self.assertIn('A text message confirming your registration should arrive soon', contents)

    async def get_register(self, display_region):
        url_get = self.get_url_from_class('Register', 'get', display_region=display_region)
        with self.assertLogs('respondent-home', 'INFO') as cm:
            get_response = await self.client.request('GET', url_get)
            self.assertLogEvent(cm, self.build_url_log_entry('', display_region, 'GET',
                                                             include_request_type=False, include_page=False))
            self.assertEqual(get_response.status, 200)
            self.check_content_register(display_region, str(await get_response.content.read()))

    async def get_register_start(self, display_region):
        url_get = self.get_url_from_class('RegisterStart', 'get', display_region=display_region, request_type='person')
        with self.assertLogs('respondent-home', 'INFO') as cm:
            get_response = await self.client.request('GET', url_get)
            self.assertLogEvent(cm, self.build_url_log_entry('start', display_region, 'GET',
                                                             include_request_type=True, include_page=True))
            self.assertEqual(get_response.status, 200)
            self.check_content_register_start(display_region, str(await get_response.content.read()))

    async def post_register_start(self, display_region):
        url_post = self.get_url_from_class('RegisterStart', 'post',
                                           display_region=display_region, request_type='person')
        with self.assertLogs('respondent-home', 'INFO') as cm:
            get_response = await self.client.request('POST', url_post)
            self.assertLogEvent(cm, self.build_url_log_entry('start', display_region, 'POST',
                                                             include_request_type=True, include_page=True))
            self.assertLogEvent(cm, self.build_url_log_entry('consent', display_region, 'GET',
                                                             include_request_type=True, include_page=True))
            self.assertEqual(get_response.status, 200)
            self.check_content_register_consent(display_region, str(await get_response.content.read()))

    async def post_register_consent_accept(self, display_region):
        url_post = self.get_url_from_class('RegisterConsent', 'post',
                                           display_region=display_region, request_type='person')
        data = {'button-accept': 'accept'}
        with self.assertLogs('respondent-home', 'INFO') as cm:
            get_response = await self.client.request('POST', url_post, data=data)
            self.assertLogEvent(cm, self.build_url_log_entry('consent', display_region, 'POST',
                                                             include_request_type=True, include_page=True))
            self.assertLogEvent(cm, self.build_url_log_entry('enter-mobile', display_region, 'GET',
                                                             include_request_type=True, include_page=True))
            self.assertEqual(get_response.status, 200)
            self.check_content_register_enter_mobile(display_region, str(await get_response.content.read()))

    async def post_register_consent_declined(self, display_region):
        url_post = self.get_url_from_class('RegisterConsent', 'post',
                                           display_region=display_region, request_type='person')
        data = {'button-decline': 'decline'}
        with self.assertLogs('respondent-home', 'INFO') as cm:
            get_response = await self.client.request('POST', url_post, data=data)
            self.assertLogEvent(cm, self.build_url_log_entry('consent', display_region, 'POST',
                                                             include_request_type=True, include_page=True))
            self.assertLogEvent(cm, self.build_url_log_entry('consent-declined', display_region, 'GET',
                                                             include_request_type=True, include_page=True))
            self.assertEqual(get_response.status, 200)
            self.check_content_register_consent_declined(display_region, str(await get_response.content.read()))

    async def post_register_consent_invalid(self, display_region):
        url_post = self.get_url_from_class('RegisterConsent', 'post',
                                           display_region=display_region, request_type='person')
        data = {}
        with self.assertLogs('respondent-home', 'INFO') as cm:
            get_response = await self.client.request('POST', url_post, data=data)
            self.assertLogEvent(cm, self.build_url_log_entry('consent', display_region, 'POST',
                                                             include_request_type=True, include_page=True))
            self.assertLogEvent(cm, self.build_url_log_entry('consent', display_region, 'GET',
                                                             include_request_type=True, include_page=True))
            self.assertEqual(get_response.status, 200)
            self.check_content_register_consent(display_region, str(await get_response.content.read()))

    async def post_register_enter_mobile_valid(self, display_region):
        url_post = self.get_url_from_class('RegisterEnterMobile', 'post',
                                           display_region=display_region, request_type='person')
        data = {'request-mobile-number': self.mobile_valid, 'action[save_continue]': ''}
        with self.assertLogs('respondent-home', 'INFO') as cm:
            get_response = await self.client.request('POST', url_post, data=data)
            self.assertLogEvent(cm, self.build_url_log_entry('enter-mobile', display_region, 'POST',
                                                             include_request_type=True, include_page=True))
            self.assertLogEvent(cm, 'valid mobile number')
            self.assertLogEvent(cm, self.build_url_log_entry('confirm-registration', display_region, 'GET',
                                                             include_request_type=True, include_page=True))
            self.assertEqual(get_response.status, 200)
            self.check_content_register_confirm_registration(display_region, str(await get_response.content.read()))

    async def post_register_enter_mobile_empty(self, display_region):
        url_post = self.get_url_from_class('RegisterEnterMobile', 'post',
                                           display_region=display_region, request_type='person')
        data = {'request-mobile-number': '', 'action[save_continue]': ''}
        with self.assertLogs('respondent-home', 'INFO') as cm:
            get_response = await self.client.request('POST', url_post, data=data)
            self.assertLogEvent(cm, self.build_url_log_entry('enter-mobile', display_region, 'POST',
                                                             include_request_type=True, include_page=True))
            self.assertLogEvent(cm, self.build_url_log_entry('enter-mobile', display_region, 'GET',
                                                             include_request_type=True, include_page=True))
            self.assertEqual(get_response.status, 200)
            self.check_content_register_enter_mobile(display_region, str(await get_response.content.read()),
                                                     error='empty')

    async def post_register_enter_mobile_invalid(self, display_region):
        url_post = self.get_url_from_class('RegisterEnterMobile', 'post',
                                           display_region=display_region, request_type='person')
        data = {'request-mobile-number': 'xxxxxx', 'action[save_continue]': ''}
        with self.assertLogs('respondent-home', 'INFO') as cm:
            get_response = await self.client.request('POST', url_post, data=data)
            self.assertLogEvent(cm, self.build_url_log_entry('enter-mobile', display_region, 'POST',
                                                             include_request_type=True, include_page=True))
            self.assertLogEvent(cm, self.build_url_log_entry('enter-mobile', display_region, 'GET',
                                                             include_request_type=True, include_page=True))
            self.assertEqual(get_response.status, 200)
            self.check_content_register_enter_mobile(display_region, str(await get_response.content.read()),
                                                     error='invalid')

    async def post_register_confirm_registration_yes(self, display_region):
        url_post = self.get_url_from_class('RegisterConfirmRegistration', 'post',
                                           display_region=display_region, request_type='person')
        data = {'request-mobile-confirmation': 'yes', 'action[save_continue]': ''}
        with self.assertLogs('respondent-home', 'INFO') as cm:
            get_response = await self.client.request('POST', url_post, data=data)
            self.assertLogEvent(cm, self.build_url_log_entry('confirm-registration', display_region, 'POST',
                                                             include_request_type=True, include_page=True))
            self.assertLogEvent(cm, self.build_url_log_entry('complete', display_region, 'GET',
                                                             include_request_type=True, include_page=True))
            self.assertEqual(get_response.status, 200)
            self.check_content_register_complete(display_region, str(await get_response.content.read()))

    async def post_register_confirm_registration_no(self, display_region):
        url_post = self.get_url_from_class('RegisterConfirmRegistration', 'post',
                                           display_region=display_region, request_type='person')
        data = {'request-mobile-confirmation': 'no', 'action[save_continue]': ''}
        with self.assertLogs('respondent-home', 'INFO') as cm:
            get_response = await self.client.request('POST', url_post, data=data)
            self.assertLogEvent(cm, self.build_url_log_entry('confirm-registration', display_region, 'POST',
                                                             include_request_type=True, include_page=True))
            self.assertLogEvent(cm, self.build_url_log_entry('enter-mobile', display_region, 'GET',
                                                             include_request_type=True, include_page=True))
            self.assertEqual(get_response.status, 200)
            self.check_content_register_enter_mobile(display_region, str(await get_response.content.read()))

    async def post_register_confirm_registration_missing(self, display_region):
        url_post = self.get_url_from_class('RegisterConfirmRegistration', 'post',
                                           display_region=display_region, request_type='person')
        data = {}
        with self.assertLogs('respondent-home', 'INFO') as cm:
            get_response = await self.client.request('POST', url_post, data=data)
            self.assertLogEvent(cm, self.build_url_log_entry('confirm-registration', display_region, 'POST',
                                                             include_request_type=True, include_page=True))
            self.assertLogEvent(cm, self.build_url_log_entry('confirm-registration', display_region, 'GET',
                                                             include_request_type=True, include_page=True))
            self.assertEqual(get_response.status, 200)
            self.check_content_register_confirm_registration(display_region, str(await get_response.content.read()),
                                                             error='empty')

    async def post_register_confirm_registration_invalid(self, display_region):
        url_post = self.get_url_from_class('RegisterConfirmRegistration', 'post',
                                           display_region=display_region, request_type='person')
        data = {'request-mobile-confirmation': 'cheese', 'action[save_continue]': ''}
        with self.assertLogs('respondent-home', 'INFO') as cm:
            get_response = await self.client.request('POST', url_post, data=data)
            self.assertLogEvent(cm, self.build_url_log_entry('confirm-registration', display_region, 'POST',
                                                             include_request_type=True, include_page=True))
            self.assertLogEvent(cm, self.build_url_log_entry('confirm-registration', display_region, 'GET',
                                                             include_request_type=True, include_page=True))
            self.assertEqual(get_response.status, 200)
            self.check_content_register_confirm_registration(display_region, str(await get_response.content.read()),
                                                             error='invalid')

    @unittest_run_loop
    async def test_register_basic_happy_path_en(self):
        display_region = 'en'
        await self.get_register(display_region)
        await self.get_register_start(display_region)
        await self.post_register_start(display_region)
        await self.post_register_consent_accept(display_region)
        await self.post_register_enter_mobile_valid(display_region)
        await self.post_register_confirm_registration_yes(display_region)

    @unittest_run_loop
    async def test_register_consent_declined_en(self):
        display_region = 'en'
        await self.get_register_start(display_region)
        await self.post_register_start(display_region)
        await self.post_register_consent_declined(display_region)

    @unittest_run_loop
    async def test_register_consent_invalid_en(self):
        display_region = 'en'
        await self.get_register_start(display_region)
        await self.post_register_start(display_region)
        await self.post_register_consent_invalid(display_region)

    @unittest_run_loop
    async def test_register_mobile_empty_en(self):
        display_region = 'en'
        await self.get_register_start(display_region)
        await self.post_register_start(display_region)
        await self.post_register_consent_accept(display_region)
        await self.post_register_enter_mobile_empty(display_region)

    @unittest_run_loop
    async def test_register_mobile_invalid_en(self):
        display_region = 'en'
        await self.get_register_start(display_region)
        await self.post_register_start(display_region)
        await self.post_register_consent_accept(display_region)
        await self.post_register_enter_mobile_invalid(display_region)

    @unittest_run_loop
    async def test_register_confirm_registration_no_en(self):
        display_region = 'en'
        await self.get_register_start(display_region)
        await self.post_register_start(display_region)
        await self.post_register_consent_accept(display_region)
        await self.post_register_enter_mobile_valid(display_region)
        await self.post_register_confirm_registration_no(display_region)

    @unittest_run_loop
    async def test_register_confirm_registration_empty_en(self):
        display_region = 'en'
        await self.get_register_start(display_region)
        await self.post_register_start(display_region)
        await self.post_register_consent_accept(display_region)
        await self.post_register_enter_mobile_valid(display_region)
        await self.post_register_confirm_registration_missing(display_region)

    @unittest_run_loop
    async def test_register_confirm_registration_invalid_en(self):
        display_region = 'en'
        await self.get_register_start(display_region)
        await self.post_register_start(display_region)
        await self.post_register_consent_accept(display_region)
        await self.post_register_enter_mobile_valid(display_region)
        await self.post_register_confirm_registration_invalid(display_region)
