import asyncio
import functools
import json
import time
import uuid

from aiohttp.test_utils import AioHTTPTestCase
from tenacity import wait_exponential

from app import app

from app import session, request
from aiohttp_session import session_middleware
from aiohttp_session import SimpleCookieStorage


def skip_build_eq(func, *args, **kwargs):
    """
    Helper decorator for manually patching the methods of app.eq.EqPayloadConstructor.

    This can be useful for tests that perform as a client but wish the server to skip the builder functionality.

    The test case checks for and calls when possible .setUp and .tearDown attributes on each test method
    at server setUp (setUpAsync) and server tearDown (tearDownAsync).

    :param func: test method that requires the patch
    :param args: the test method's arguments
    :param args: the test method's keyword arguments
    :return: new method with patching functions attached as attributes
    """
    async def _override_eq_payload_constructor(test_case, *_):
        from app import eq

        async def build(_):
            return test_case.eq_payload

        eq.EqPayloadConstructor._bk__init__ = eq.EqPayloadConstructor.__init__
        eq.EqPayloadConstructor.__init__ = lambda *args: None
        eq.EqPayloadConstructor._bk_build = eq.EqPayloadConstructor.build
        eq.EqPayloadConstructor.build = build

    async def _reset_eq_payload_constructor(*_):
        from app import eq

        eq.EqPayloadConstructor.__init__ = eq.EqPayloadConstructor._bk__init__
        eq.EqPayloadConstructor.build = eq.EqPayloadConstructor._bk_build

    @functools.wraps(func, *args, **kwargs)
    def new_func(self, *inner_args, **inner_kwargs):
        return func(self, *inner_args, **inner_kwargs)

    new_func.setUp = _override_eq_payload_constructor
    new_func.tearDown = _reset_eq_payload_constructor

    return new_func


def build_eq_raises(func, *args, **kwargs):
    """
    Helper decorator for manually patching the methods of app.eq.EqPayloadConstructor.

    This can be useful for tests that perform as a client but wish the server to raise InvalidEqPayLoad when .build()
    is called on an instance of app.eq.EqPayloadConstructor.

    The test case checks for and calls when possible .setUp and .tearDown attributes on each test method
    at server setUp (setUpAsync) and server tearDown (tearDownAsync).

    :param func: test method that requires the patch
    :param args: the test method's arguments
    :param args: the test method's keyword arguments
    :return: new method with patching functions attached as attributes
    """
    async def _override_eq_build_with_error(*_):
        from app import eq

        async def build(_):
            raise eq.InvalidEqPayLoad('')

        eq.EqPayloadConstructor._bk__init__ = eq.EqPayloadConstructor.__init__
        eq.EqPayloadConstructor.__init__ = lambda *args: None
        eq.EqPayloadConstructor._bk_build = eq.EqPayloadConstructor.build
        eq.EqPayloadConstructor.build = build

    async def _reset_eq_payload_constructor(*_):
        from app import eq

        eq.EqPayloadConstructor.__init__ = eq.EqPayloadConstructor._bk__init__
        eq.EqPayloadConstructor.build = eq.EqPayloadConstructor._bk_build

    @functools.wraps(func, *args, **kwargs)
    def new_func(self, *inner_args, **inner_kwargs):
        return func(self, *inner_args, **inner_kwargs)

    new_func.setUp = _override_eq_build_with_error
    new_func.tearDown = _reset_eq_payload_constructor

    return new_func


def skip_encrypt(func, *args, **kwargs):
    """
    Helper decorator for manually patching the encrypt function in start_handlers.py.

    This can be useful for tests that perform as a client but wish the server to skip encrypting a payload.

    The test case checks for and calls when possible .setUp and .tearDown attributes on each test method
    at server setUp (setUpAsync) and server tearDown (tearDownAsync).

    :param func: test method that requires the patch
    :param args: the test method's arguments
    :param args: the test method's keyword arguments
    :return: new method with patching functions attached as attributes
    """
    async def _override_sdc_encrypt(*_):
        from app import utils

        def encrypt(payload, **_):
            return json.dumps(payload)

        utils._bk_encrypt = utils.encrypt
        utils.encrypt = encrypt

    async def _reset_sdc_encrypt(*_):
        from app import utils

        utils.encrypt = utils._bk_encrypt

    @functools.wraps(func, *args, **kwargs)
    def new_func(self, *inner_args, **inner_kwargs):
        return func(self, *inner_args, **inner_kwargs)

    new_func.setUp = _override_sdc_encrypt
    new_func.tearDown = _reset_sdc_encrypt

    return new_func


class RHTestCase(AioHTTPTestCase):

    language_code = 'en'
    response_id = '2vfBHlIsGPImYlWTvXLiBeXw14NkzoicZcDJB8pZ9FQ='

    start_date = '2018-04-10'
    end_date = '2020-05-31'
    return_by = '2018-05-08'

    def session_storage(self, app_config):
        self.assertIn('REDIS_SERVER', app_config)
        self.assertIn('REDIS_PORT', app_config)
        self.assertIn('SESSION_AGE', app_config)
        return session_middleware(
            SimpleCookieStorage(cookie_name='RH_SESSION'))

    async def get_application(self):
        # Monkey patch the session setup function to remove Redis dependency for unit tests
        session.setup = self.session_storage
        # Monkey patch request retry wait time for faster tests
        request.RetryRequest._request_using_pool.retry.wait = wait_exponential(multiplier=0)
        request.RetryRequest._request_basic.retry.wait = wait_exponential(multiplier=0)
        return app.create_app('TestingConfig')

    async def setUpAsync(self):
        test_method = getattr(self, self._testMethodName)
        if hasattr(test_method, 'setUp'):
            await test_method.setUp(self)

    async def tearDownAsync(self):
        test_method = getattr(self, self._testMethodName)
        if hasattr(test_method, 'tearDown'):
            await test_method.tearDown(self)

    def assertLogJson(self, watcher, event, **kwargs):
        """
        Helper method for asserting the contents of structlog records caught by self.assertLogs.

        Fails if no match is found. A match is based on the main log message (event) and all additional
        items passed in kwargs.

        :param watcher: context manager returned by `with self.assertLogs(LOGGER, LEVEL)`
        :param event: event logged; use empty string to ignore or no message
        :param kwargs: other structlog key value pairs to assert for
        """
        for record in watcher.records:
            message_json = json.loads(record.message)
            try:
                if (event in message_json.get('event', '')
                        and all(message_json[key] == val
                                for key, val in kwargs.items())):
                    break
            except KeyError:
                pass
        else:
            self.fail(f'No matching log records present: {event}')

    def assertLogEvent(self, watcher, event, **kwargs):
        """
        Helper method for asserting the contents of RH records caught by self.assertLogs.

        Fails if no match is found. A match is based on the static message string (event) and all additional
        items passed in kwargs.

        :param watcher: context manager returned by `with self.assertLogs(LOGGER, LEVEL)`
        :param event: event logged; use empty string to ignore or no message
        :param kwargs: other structlog key value pairs to assert for
        """
        for record in watcher.records:
            try:
                if (event in record.message
                        and all(record.__dict__[key] == val
                                for key, val in kwargs.items())):
                    return record
            except KeyError:
                pass
        else:
            self.fail(
                f"No matching log records with event: '{event}' and parameters: {kwargs}"
            )

    def assertMessagePanel(self, message, content):
        """
        Helper method for asserting the rendered content includes the required message panels.

        :param message: message dict
        :param content: rendered HTML str
        """
        if message.get('clickable', False):
            self.assertIn('js-inpagelink', content)

        for message_line in message['text'].split('\n'):
            self.assertIn(message_line, content)

        level = message['level'].lower()
        self.assertIn(f'panel--{level}', content)

    def assertSiteLogo(self, display_region, content):
        """
        Helper method for asserting that the correct site logo is presented (english or welsh)
        :param display_region: str: either 'en' or 'cy'
        :param content: rendered HTML str
        """
        if display_region == 'cy':
            self.assertIn('<title id="ons-logo-cy-alt">', content)
        else:
            self.assertIn('<title id="ons-logo-en-alt">', content)

    def assertExitButton(self, display_region, content):
        """
        Helper method for asserting that the 'Exit' button is presented (english or welsh) on authenticated pages
        :param display_region: str: either 'en' or 'cy'
        :param content: rendered HTML str
        """
        if display_region == 'cy':
            self.assertIn('href="/cy/start/exit/"', content)
        else:
            self.assertIn('href="/en/start/exit/"', content)

    def assertNotExitButton(self, display_region, content):
        """
        Helper method for asserting that the 'Exit' button is presented (english or welsh) on authenticated pages
        :param display_region: str: either 'en' or 'cy'
        :param content: rendered HTML str
        """
        if display_region == 'cy':
            self.assertNotIn('href="/cy/start/exit/"', content)
        else:
            self.assertNotIn('href="/en/start/exit/"', content)

    def assertCorrectHeadTitleTag(self, display_region, title, content, error=False):
        """
        Helper method for asserting that the head title tag is correct and displays error prefix if required
        :param display_region: str: either 'en' or 'cy'
        :param title: str
        :param content: rendered HTML str
        :param error: Boolean
        """
        if display_region == 'cy':
            site_name = self.app['SITE_NAME_CY']
            error_prefix = 'Gwall'
        else:
            site_name = self.app['SITE_NAME_EN']
            error_prefix = 'Error'
        if error:
            self.assertIn('<title>' + error_prefix + ': ' + title + ' - ' + site_name + '</title>', content)
        else:
            self.assertIn('<title>' + title + ' - ' + site_name + '</title>', content)

    def assertCorrectQuestionText(self, title, content):
        """
        Helper method for asserting that the question title is correct (h1 tag)
        :param title: str
        :param content: rendered HTML str
        """
        self.assertIn('<h1 id="question-title" class="ons-question__title">' + title + '</h1>', content)

    def assertCorrectPageTitle(self, title, content):
        """
        Helper method for asserting that the question title is correct (h1 tag)
        :param title: str
        :param content: rendered HTML str
        """
        self.assertIn('<h1 class="ons-u-mb-xs ons-u-fs-l">' + title + '</h1>', content)

    def assertErrorMessageDisplayed(self, display_region, panel_label, list_error, field_name, field_error, content):
        """
        Helper method for asserting that the error panel and messages are displayed
        :param display_region: str: either 'en' or 'cy'
        :param panel_label: str: either 'answer' or 'response'
        :param list_error: str: text of error in red panel
        :param field_name: str: field error is reported on
        :param field_error: str: text of error on individual field
        :param content: rendered HTML str
        """
        if display_region == 'cy':
            if panel_label == 'answer':
                panel_label_text = "Mae problem gyda\\\'ch ateb"
            else:
                panel_label_text = "Mae problem gyda\\\'r dudalen hon"
        else:
            if panel_label == 'answer':
                panel_label_text = 'There is a problem with your answer'
            else:
                panel_label_text = 'There is a problem with this page'

        self.assertIn('<h2 id="error-summary-title" data-qa="error-header" class="ons-panel__title ons-u-fs-r--b">'
                      + panel_label_text + '</h2>', content)
        self.assertIn('<a href="#' + field_name + '" class="ons-list__link  js-inpagelink">' + list_error + '</a>',
                      content)
        self.assertIn('<strong>' + field_error + '</strong>', content)

    def assertCorrectTranslationLink(self, content, display_region, user_journey, request_type=None, page=None):
        """
        Helper method for asserting that the correct translation link is displayed
        :param display_region: str: either 'en' or 'cy'
        :param user_journey: str
        :param content: rendered HTML str
        :param request_type: str
        :param page: str
        """
        if display_region == 'cy':
            lang = 'en'
            link_text = 'English'
        else:
            lang = 'cy'
            link_text = 'Cymraeg'

        if not page:
            link = '<a href="/' + lang + '/' + user_journey + '/" lang="' + lang + '" >' + link_text + '</a>'
        elif not request_type:
            link = '<a href="/' + lang + '/' + user_journey + '/' + page + \
                   '/" lang="' + lang + '" >' + link_text + '</a>'
        else:
            link = '<a href="/' + lang + '/' + user_journey + '/' + request_type + '/' + page + \
                   '/" lang="' + lang + '" >' + link_text + '</a>'

        self.assertIn(link, content)

    def assert500Error(self, response, display_region, content, check_exit=False):
        """
        Helper method for asserting that the correct site logo is presented (english or welsh)
        :param response: obj
        :param display_region: str: either 'en' or 'cy'
        :param content: rendered HTML str
        :param check_exit: Boolean
        """
        self.assertEqual(response.status, 500)
        self.assertSiteLogo(display_region, content)
        if not check_exit:
            self.assertNotExitButton(display_region, content)
        if display_region == 'cy':
            self.assertIn("Mae\\'n flin gennym, aeth rhywbeth o\\'i le", content)
        else:
            self.assertIn('Sorry, something went wrong', content)

    def setUp(self):
        # This section gets ugly if YAPF reformats it
        # yapf: disable
        super().setUp()  # NB: setUp the server first so we can use self.app
        with open('tests/test_data/rhsvc/uac_e.json') as fp:
            self.uac_json_e = json.load(fp)

        with open('tests/test_data/rhsvc/uac-w.json') as fp:
            self.uac_json_w = json.load(fp)

        # URLs used in later statements
        url_path_prefix = self.app['URL_PATH_PREFIX']
        account_svc_url = self.app['ACCOUNT_SERVICE_URL']
        rh_svc_url = self.app['RHSVC_URL']
        address_index_svc_url = self.app['ADDRESS_INDEX_SVC_URL']
        aims_epoch = self.app['ADDRESS_INDEX_EPOCH']

        site_name_en = self.app['SITE_NAME_EN']
        site_name_cy = self.app['SITE_NAME_CY']

        self.aims_postcode_limit = '5000'

        self.get_info = self.app.router['Info:get'].url_for()

        # Common

        # Test Data

        self.postcode_valid = 'EX2 6GA'
        self.postcode_invalid = 'ZZ99 9ZZ'
        self.postcode_no_results = 'GU34 6DU'
        self.postcode_empty = ''
        self.adlocation = '1234567890'

        self.selected_uprn = '10023122451'

        self.mobile_valid = '07012345678'
        self.mobile_invalid_short = '07012'
        self.mobile_invalid_long = '0701234567890123456'
        self.mobile_invalid_character = '0701234567$'

        self.email_valid = 'test@testing.com'
        self.email_invalid = 'cheese.scone'

        self.field_empty = None

        self.common_form_data_empty = {}

        self.content_common_invalid_mobile_error_en = \
            'Enter a UK mobile number in a valid format, for example, 07700 900345 or +44 7700 900345'
        self.content_common_invalid_mobile_error_cy = \
            "Rhowch rif ffôn symudol yn y Deyrnas Unedig mewn fformat dilys, er enghraifft, " \
            "07700 900345 neu +44 7700 900345"

        self.common_select_address_input_valid = {
            'form-pick-address': '10023122451', 'action[save_continue]': '',
        }

        self.common_select_address_input_not_listed = {
            'form-pick-address': 'xxxx', 'action[save_continue]': '',
        }

        self.common_confirm_address_input_yes = {
            'form-confirm-address': 'yes', 'action[save_continue]': ''
        }

        self.common_confirm_address_input_no = {
            'form-confirm-address': 'no', 'action[save_continue]': ''
        }

        self.common_confirm_address_input_invalid = {
            'form-confirm-address': 'invalid', 'action[save_continue]': ''
        }

        self.common_postcode_input_valid = {
            'form-enter-address-postcode': self.postcode_valid, 'action[save_continue]': '',
        }

        self.common_postcode_input_no_results = {
            'form-enter-address-postcode': self.postcode_no_results, 'action[save_continue]': '',
        }

        self.common_postcode_input_invalid = {
            'form-enter-address-postcode': self.postcode_invalid, 'action[save_continue]': '',
        }

        self.common_postcode_input_empty = {
            'form-enter-address-postcode': self.postcode_empty, 'action[save_continue]': '',
        }

        self.common_address_finder_input = {
            'address-uprn': self.selected_uprn, 'action[save_continue]': '',
        }

        with open('tests/test_data/address_index/postcode_no_results.json') as fp:
            f = asyncio.Future()
            f.set_result(json.load(fp))
            self.ai_postcode_no_results = f

        with open('tests/test_data/address_index/postcode_results.json') as fp:
            f = asyncio.Future()
            f.set_result(json.load(fp))
            self.ai_postcode_results = f

        with open('tests/test_data/address_index/uprn_valid_hh.json') as fp:
            f = asyncio.Future()
            f.set_result(json.load(fp))
            self.ai_uprn_result_hh = f

        with open('tests/test_data/address_index/uprn_england.json') as fp:
            f = asyncio.Future()
            f.set_result(json.load(fp))
            self.ai_uprn_result_england = f

        with open('tests/test_data/address_index/uprn_wales.json') as fp:
            f = asyncio.Future()
            f.set_result(json.load(fp))
            self.ai_uprn_result_wales = f

        # Content
        self.content_call_centre_number_ew = '0800 141 2021'
        self.content_call_centre_number_cy = '0800 169 2021'

        self.content_common_select_address_no_results_en = 'Sorry, there was a problem processing your postcode'
        self.content_common_select_address_no_results_cy = \
            "Mae\\\'n ddrwg gennym, roedd problem wrth brosesu eich cod post"

        self.content_common_contact_centre_title_en = 'You need to call the customer contact centre'
        self.content_common_contact_centre_title_cy = 'You need to call the customer contact centre'

        self.content_common_404_error_title_en = 'Page not found'
        self.content_common_404_error_secondary_en = 'If you entered a web address, check it is correct.'
        self.content_common_404_error_title_cy = "Heb ddod o hyd i\\\'r dudalen"
        self.content_common_404_error_secondary_cy = \
            "Os gwnaethoch chi roi cyfeiriad gwe, gwnewch yn si\\xc5\\xb5r ei fod yn gywir."

        self.content_common_timeout_en = 'Your session has timed out due to inactivity'
        self.content_common_timeout_cy = 'Mae eich sesiwn wedi cyrraedd y terfyn amser oherwydd anweithgarwch'

        self.content_common_429_error_eq_launch_title_en = \
            'We are currently experiencing very high demand, thank you for your patience'
        self.content_common_429_error_uac_title_en = \
            'You have reached the maximum number of access codes you can request online'
        self.content_common_429_error_eq_launch_title_cy = \
            "Rydym ni\\\'n brysur iawn ar hyn o bryd, diolch am eich amynedd"
        self.content_common_429_error_uac_title_cy = \
            "Rydych chi wedi cyrraedd y nifer fwyaf o godau mynediad y gallwch ofyn amdanynt ar lein"

        # End Common

        # Start Journey

        # Content
        self.content_start_uac_already_used_en = 'This access code has already been used'
        self.content_start_uac_already_used_cy = "Mae\\\'r cod mynediad hwn eisoes wedi cael ei ddefnyddio"

        self.content_start_confirm_address_page_title_en = '<title>Confirm address - ' + site_name_en + '</title>'
        self.content_start_confirm_address_page_title_error_en = \
            '<title>Error: Confirm address - ' + site_name_en + '</title>'
        self.content_start_confirm_address_title_en = 'Is this the correct address?'
        self.content_start_confirm_address_option_yes_en = 'Yes, this is the correct address'
        self.content_start_confirm_address_option_no_en = 'No, this is not the correct address'
        self.content_start_confirm_address_error_en = 'Select an answer'
        self.content_start_confirm_address_page_title_cy = '<title>Cadarnhau cyfeiriad - ' + site_name_cy + '</title>'
        self.content_start_confirm_address_page_title_error_cy = \
            '<title>Gwall: Cadarnhau cyfeiriad - ' + site_name_cy + '</title>'
        self.content_start_confirm_address_title_cy = "Ai dyma\\\'r cyfeiriad cywir?"
        self.content_start_confirm_address_option_yes_cy = "Ie, dyma\\\'r cyfeiriad cywir"
        self.content_start_confirm_address_option_no_cy = "Na, nid dyma\\\'r cyfeiriad cywir"
        self.content_start_confirm_address_error_cy = "Dewiswch ateb"

        self.content_start_incorrect_address_page_title_en = \
            '<title>You do not need to take part in this study - ' + site_name_en + '</title>'
        self.content_start_incorrect_address_title_en = 'You do not need to take part in this study'
        self.content_start_incorrect_address_page_title_cy = \
            "<title>You do not need to take part in this study - " + site_name_cy + "</title>"
        self.content_start_incorrect_address_title_cy = 'You do not need to take part in this study'

        self.content_signed_out_page_title_en = '<title>Progress saved - ' + site_name_en + '</title>'
        self.content_signed_out_title_en = 'Your progress has been saved'
        self.content_signed_out_page_title_cy = "<title>Cynnydd wedi&#39;i gadw - " + site_name_cy + "</title>"
        self.content_signed_out_title_cy = 'Mae eich cynnydd wedi cael ei gadw'

        self.content_start_timeout_title_en = 'Your session has timed out due to inactivity'
        self.content_start_timeout_title_cy = 'Mae eich sesiwn wedi cyrraedd y terfyn amser oherwydd anweithgarwch'
        self.content_start_timeout_bullet_one_en = 'To protect your information we have timed you out'
        self.content_start_timeout_bullet_one_cy = \
            'Er mwyn diogelu eich gwybodaeth, mae eich sesiwn wedi cyrraedd y terfyn amser'
        self.content_start_timeout_restart_en = 'enter your 16-character access code'
        self.content_start_timeout_restart_cy = 'eich cod mynediad 16 node'

        self.content_start_forbidden_title_en = 'Sorry, there is a problem'
        self.content_start_timeout_forbidden_link_text_en = 'enter your 16-character access code'
        self.content_start_forbidden_title_cy = "Mae\\\'n ddrwg gennym, mae problem wedi codi"
        self.content_start_timeout_forbidden_link_text_cy = "eich cod mynediad 16 nod"

        self.content_start_closed_study = "Your access code is for a study that has now closed."

        # End Start Journey

        # Session Timeout

        self.content_start_timeout_title_en = 'Sorry, you need to enter your access code'
        self.content_start_timeout_title_cy = "Mae\\\'n ddrwg gennym, bydd angen i chi roi eich cod mynediad"
        self.content_start_timeout_bullet_one_en = \
            'been inactive for 45 minutes and your session has timed out to protect your information'
        self.content_start_timeout_bullet_one_cy = \
            "wedi bod yn anweithgar am 45 munud a bod eich sesiwn wedi cyrraedd y terfyn " \
            "amser er mwyn diogelu eich gwybodaeth, neu"
        self.content_start_timeout_bullet_two_en = \
            'followed a link to the middle of a study questionnaire'
        self.content_start_timeout_bullet_two_cy = \
            "followed a link to the middle of a study questionnaire"
        self.content_start_timeout_link_text_en = 'enter your 16-character access code'
        self.content_start_timeout_link_text_cy = "enter your 16-character access code"

        self.content_request_timeout_title_en = 'Sorry, you need to start again'
        self.content_request_timeout_title_cy = "Mae\\\'n ddrwg gennym, mae angen i chi ddechrau eto"
        self.content_request_timeout_bullet_one_en = \
            'been inactive for 45 minutes and your session has timed out to protect your information'
        self.content_request_timeout_bullet_one_cy = \
            "wedi bod yn anweithgar am 45 munud a bod eich sesiwn wedi cyrraedd y " \
            "terfyn amser er mwyn diogelu eich gwybodaeth, neu "
        self.content_request_code_timeout_bullet_two_en = \
            'followed a link to the middle of a request for a new access code'
        self.content_request_code_timeout_bullet_two_cy = \
            "wedi dilyn dolen i ganol cais am god mynediad newydd"
        self.content_request_code_timeout_link_text_en = 'request a new access code'
        self.content_request_code_timeout_link_text_cy = "ofyn am god mynediad newydd"

        # End Session Timeout

        self.get_start_en = self.app.router['Start:get'].url_for(display_region='en')
        self.post_start_en = self.app.router['Start:post'].url_for(display_region='en')
        self.get_start_confirm_address_en = self.app.router['StartConfirmAddress:get'].url_for(display_region='en')
        self.post_start_confirm_address_en = self.app.router['StartConfirmAddress:post'].url_for(display_region='en')

        self.get_start_cy = self.app.router['Start:get'].url_for(display_region='cy')
        self.post_start_cy = self.app.router['Start:post'].url_for(display_region='cy')
        self.get_start_confirm_address_cy = self.app.router['StartConfirmAddress:get'].url_for(display_region='cy')
        self.post_start_confirm_address_cy = self.app.router['StartConfirmAddress:post'].url_for(display_region='cy')

        self.get_signed_out_en = self.app.router['SignedOut:get'].url_for(display_region='en')
        self.get_signed_out_cy = self.app.router['SignedOut:get'].url_for(display_region='cy')

        self.case_id = self.uac_json_e['collectionCase']['caseId']
        self.collection_exercise_id = self.uac_json_e['collectionExercise']['collectionExerciseId']
        self.eq_id = '9999'
        self.form_type = 'zzz'
        self.jti = str(uuid.uuid4())
        self.uac_code = ''.join([str(n) for n in range(13)])
        self.uac1, self.uac2, self.uac3, self.uac4 = \
            self.uac_code[:4], self.uac_code[4:8], self.uac_code[8:12], self.uac_code[12:]
        self.period_id = '2021'
        self.uac = 'w4nwwpphjjptp7fn'
        self.uacHash = self.uac_json_e['uacHash']
        self.uprn = self.uac_json_e['collectionCase']['address']['uprn']
        self.response_id = '111000000092a445af12905967d'
        self.questionnaire_id = self.uac_json_e['qid']
        self.channel = 'rh'
        self.attributes_en = {
            'addressLine1': self.uac_json_e['collectionCase']['address']['addressLine1'],
            'addressLine2': self.uac_json_e['collectionCase']['address']['addressLine2'],
            'addressLine3': self.uac_json_e['collectionCase']['address']['addressLine3'],
            'townName': self.uac_json_e['collectionCase']['address']['townName'],
            'postcode': self.uac_json_e['collectionCase']['address']['postcode'],
            'uprn': self.uac_json_e['collectionCase']['address']['uprn'],
            'language': 'en',
            'display_region': 'en'
        }
        self.attributes_cy = {
            **self.attributes_en,
            'language': 'cy',
            'display_region': 'cy',
            'locale': 'cy'
        }

        self.eq_payload = {
            'jti': self.jti,
            'tx_id': self.jti,
            'iat': int(time.time()),
            'exp': int(time.time() + (5 * 60)),
            'collection_exercise_sid': self.collection_exercise_id,
            'region_code': 'GB-ENG',
            'ru_ref': self.questionnaire_id,
            'case_id': self.case_id,
            'language_code': 'en',
            'display_address':
                self.uac_json_e['collectionCase']['address']['addressLine1'] + ', ' + self.uac_json_e['collectionCase']['address']['addressLine2'],
            'response_id': self.response_id,
            'account_service_url': f'{account_svc_url}{url_path_prefix}/start/',
            'account_service_log_out_url': f'{account_svc_url}{url_path_prefix}/signed-out/',
            'channel': self.channel,
            'user_id': '',
            'questionnaire_id': self.questionnaire_id,
            'eq_id': self.eq_id,
            'period_id': self.collection_exercise_id,
            'form_type': self.form_type,
            'case_ref': '123abc',
            'period_str': 'velit',
            'schema_name': 'zzz_9999',
            'survey_url': 'https://raw.githubusercontent.com/ONSdigital/eq-questionnaire-runner/social-demo'
                          '/test_schemas/en/zzz_9999.json'
        }

        self.account_service_url = '/start/'
        self.account_service_log_out_url = '/signed-out/'

        self.survey_launched_json = {
            'questionnaireId': self.questionnaire_id,
            'caseId': self.case_id,
            'agentId': ''
        }

        self.survey_launched_json = {
            'questionnaireId': self.questionnaire_id,
            'caseId': self.case_id,
            'agentId': ''
        }

        self.rhsvc_url = (
            f'{rh_svc_url}/uacs/{self.uacHash}'
        )

        self.rhsvc_url_surveylaunched = (
            f'{rh_svc_url}/surveyLaunched'
        )

        self.rhsvc_url_fulfilments = (
            f'{rh_svc_url}/fulfilments'
        )

        self.rhsvc_cases_by_uprn_url = (
            f'{rh_svc_url}/cases/uprn/'
        )

        self.rhsvc_post_create_case_url = (
            f'{rh_svc_url}/cases/create'
        )

        self.rhsvc_put_modify_address = (
            f'{rh_svc_url}/cases/e37b0d05-3643-445e-8e71-73f7df3ff95e/address'
        )

        self.rhsvc_cases_url = (
            f'{rh_svc_url}/cases/'
        )

        self.rhsvc_new_case_url = (
            f'{rh_svc_url}/cases/new'
        )

        self.rhsvc_url_link_uac = (
            f'{rh_svc_url}/uacs/{self.uacHash}/link'
        )

        self.start_data_valid = {
            'uac': self.uac, 'action[save_continue]': '',
        }

        self.start_confirm_address_data_yes = {
            'address-check-answer': 'Yes', 'action[save_continue]': ''
        }

        self.start_confirm_address_data_no = {
            'address-check-answer': 'No', 'action[save_continue]': ''
        }

        self.start_confirm_address_data_invalid = {
            'address-check-answer': 'Invalid', 'action[save_continue]': ''
        }

        self.start_confirm_address_data_empty = {}

        self.start_modify_address_data_valid = {
            'address-line-1': 'ONS',
            'address-line-2': 'Segensworth Road',
            'address-line-3': 'Titchfield',
            'address-town': 'Fareham',
            'address-postcode': 'PO15 5RR'
        }

        self.start_modify_address_data_incomplete = {
            'address-line-2': 'Segensworth Road',
            'address-line-3': 'Titchfield',
            'address-town': 'Fareham',
            'address-postcode': 'PO15 5RR'
        }

        self.start_modify_address_data = {
            'caseId': self.case_id,
            'uprn': self.uprn,
            'addressLine1': self.uac_json_e['collectionCase']['address']['addressLine1'],
            'addressLine2': self.uac_json_e['collectionCase']['address']['addressLine2'],
            'addressLine3': self.uac_json_e['collectionCase']['address']['addressLine3'],
            'townName': self.uac_json_e['collectionCase']['address']['townName'],
            'postcode': self.uac_json_e['collectionCase']['address']['postcode']
            }

        self.content_common_error_panel_answer_en = 'There is a problem with your answer'
        self.content_common_error_panel_answer_cy = "Mae problem gyda\\\'ch ateb"
        self.content_common_error_select_an_option_en = 'Select an option'
        self.content_common_error_select_an_option_cy = 'Dewiswch opsiwn'

        self.addressindexsvc_url = f'{address_index_svc_url}/addresses/rh/postcode/'
        self.address_index_epoch_param = f'?limit={self.aims_postcode_limit}&epoch={aims_epoch}'
        self.address_index_epoch_param_test = f'?limit={self.aims_postcode_limit}&epoch=test'

        with open('tests/test_data/rhsvc/case_by_uprn_hh_e.json') as fp:
            f = asyncio.Future()
            f.set_result(json.load(fp))
            self.rhsvc_case_by_uprn_hh_e = f

        with open('tests/test_data/rhsvc/case_by_uprn_hh_w.json') as fp:
            f = asyncio.Future()
            f.set_result(json.load(fp))
            self.rhsvc_case_by_uprn_hh_w = f

        with open('tests/test_data/rhsvc/get_fulfilment_multi_sms.json') as fp:
            f = asyncio.Future()
            f.set_result(json.load(fp))
            self.rhsvc_get_fulfilment_multi_sms = f

        with open('tests/test_data/rhsvc/get_fulfilment_single_sms.json') as fp:
            f = asyncio.Future()
            f.set_result(json.load(fp))
            self.rhsvc_get_fulfilment_single_sms = f

        with open('tests/test_data/rhsvc/get_fulfilment_multi_post.json') as fp:
            f = asyncio.Future()
            f.set_result(json.load(fp))
            self.rhsvc_get_fulfilment_multi_post = f

        with open('tests/test_data/rhsvc/get_fulfilment_single_post.json') as fp:
            f = asyncio.Future()
            f.set_result(json.load(fp))
            self.rhsvc_get_fulfilment_single_post = f

        with open('tests/test_data/rhsvc/get_fulfilment_multi_email.json') as fp:
            f = asyncio.Future()
            f.set_result(json.load(fp))
            self.rhsvc_get_fulfilment_multi_email = f

        with open('tests/test_data/rhsvc/get_fulfilment_single_email.json') as fp:
            f = asyncio.Future()
            f.set_result(json.load(fp))
            self.rhsvc_get_fulfilment_single_email = f

        with open('tests/test_data/rhsvc/request_fulfilment_sms.json') as fp:
            f = asyncio.Future()
            f.set_result(json.load(fp))
            self.rhsvc_request_fulfilment_sms = f

        with open('tests/test_data/rhsvc/request_fulfilment_post.json') as fp:
            f = asyncio.Future()
            f.set_result(json.load(fp))
            self.rhsvc_request_fulfilment_post = f

        with open('tests/test_data/rhsvc/request_fulfilment_email.json') as fp:
            f = asyncio.Future()
            f.set_result(json.load(fp))
            self.rhsvc_request_fulfilment_email = f

        self.request_code_select_how_to_receive_data_sms = {
            'form-select-method': 'sms', 'action[save_continue]': ''
        }

        self.request_code_select_how_to_receive_data_post = {
            'form-select-method': 'post', 'action[save_continue]': ''
        }

        self.request_code_select_how_to_receive_data_email = {
            'form-select-method': 'email', 'action[save_continue]': ''
        }

        self.request_code_select_how_to_receive_data_invalid = {
            'form-select-method': 'invalid', 'action[save_continue]': ''
        }

        self.request_code_enter_mobile_form_data_valid = {
            'request-mobile-number': self.mobile_valid, 'action[save_continue]': '',
        }

        self.request_code_enter_mobile_form_data_invalid = {
            'request-mobile-number': self.mobile_invalid_short, 'action[save_continue]': '',
        }

        self.request_code_enter_mobile_form_data_empty = {
            'request-mobile-number': '', 'action[save_continue]': '',
        }

        self.request_code_enter_email_form_data_valid = {
            'request-email': self.email_valid, 'action[save_continue]': '',
        }

        self.request_code_enter_email_form_data_invalid = {
            'request-email': self.email_invalid, 'action[save_continue]': '',
        }

        self.request_code_enter_email_form_data_empty = {
            'request-email': '', 'action[save_continue]': '',
        }

        self.request_code_mobile_confirmation_data_yes = {
            'request-mobile-confirmation': 'yes', 'action[save_continue]': ''
        }

        self.request_code_mobile_confirmation_data_no = {
            'request-mobile-confirmation': 'no', 'action[save_continue]': ''
        }

        self.request_code_mobile_confirmation_data_invalid = {
            'request-mobile-confirmation': 'invalid', 'action[save_continue]': ''
        }

        self.request_code_mobile_confirmation_data_empty = {}

        self.request_code_email_confirmation_data_yes = {
            'request-email-confirmation': 'yes', 'action[save_continue]': ''
        }

        self.request_code_email_confirmation_data_no = {
            'request-email-confirmation': 'no', 'action[save_continue]': ''
        }

        self.request_code_email_confirmation_data_invalid = {
            'request-email-confirmation': 'invalid', 'action[save_continue]': ''
        }

        self.request_code_email_confirmation_data_empty = {}

        self.request_common_enter_name_form_data_valid = {
            'name_first_name': 'Bob', 'name_last_name': 'Bobbington', 'action[save_continue]': '',
        }

        self.request_common_enter_name_form_data_long_surname = {
            'name_first_name': 'Bob', 'name_last_name': 'Bobbington-Fortesque-Smythe',
            'action[save_continue]': '',
        }

        self.request_common_enter_name_form_data_only_spaces = {
            'name_first_name': ' ', 'name_last_name': ' ',
            'action[save_continue]': '',
        }

        self.request_common_enter_name_form_data_no_first = {
            'name_last_name': 'Bobbington', 'action[save_continue]': '',
        }

        self.request_common_enter_name_form_data_no_last = {
            'name_first_name': 'Bob', 'action[save_continue]': '',
        }

        self.request_common_enter_name_form_data_overlength_firstname = {
            'name_first_name': 'Robert Albert Everest Reginald Bartholomew', 'name_last_name': 'Bobbington',
            'action[save_continue]': '',
        }

        self.request_common_enter_name_form_data_overlength_lastname = {
            'name_first_name': 'Bob', 'name_last_name': 'Bobbington-Browning Fortesque-Smythe',
            'action[save_continue]': '',
        }

        self.content_common_enter_name_check_first = \
            'name_first_name"\\n            value="Bob"'
        self.content_common_enter_name_check_last = \
            'name_last_name"\\n            value="Bobbington"'
        self.content_common_enter_name_check_long_first = \
            'name_first_name"\\n            value="Robert Albert Everest Reginald Bartholomew"'
        self.content_common_enter_name_check_long_last = \
            'name_last_name"\\n            value="Bobbington-Browning Fortesque-Smythe"'

        self.request_common_confirm_send_by_post_data_yes = {
            'request-name-address-confirmation': 'yes', 'action[save_continue]': ''
        }

        self.request_common_confirm_send_by_post_data_yes_large_print = {
            'request-name-address-confirmation': 'yes',
            'request-name-address-large-print': 'large-print',
            'action[save_continue]': ''
        }

        self.request_common_confirm_send_by_post_data_no = {
            'request-name-address-confirmation': 'no', 'action[save_continue]': ''
        }

        self.request_common_confirm_send_by_post_data_invalid = {
            'request-name-address-confirmation': 'invalid', 'action[save_continue]': ''
        }

        self.content_request_common_enter_name_page_title_en = \
            '<title>Enter name - ' + site_name_en + '</title>'
        self.content_request_common_enter_name_page_title_error_en = \
            '<title>Error: Enter name - ' + site_name_en + '</title>'
        self.content_request_common_enter_name_title_en = 'What is your name?'
        self.content_request_common_enter_name_error_first_name_en = 'Enter your first name'
        self.content_request_common_enter_name_error_first_name_overlength_en = \
            "You have entered too many characters. Enter up to 35 characters"
        self.content_request_common_enter_name_error_last_name_en = 'Enter your last name'
        self.content_request_common_enter_name_error_last_name_overlength_en = \
            "You have entered too many characters. Enter up to 35 characters"
        self.content_request_common_enter_name_page_title_cy = \
            '<title>Nodi enw - ' + site_name_cy + '</title>'
        self.content_request_common_enter_name_page_title_error_cy = \
            '<title>Gwall: Nodi enw - ' + site_name_cy + '</title>'
        self.content_request_common_enter_name_title_cy = "Beth yw eich enw?"
        self.content_request_common_enter_name_error_first_name_cy = "Rhowch eich enw cyntaf"
        self.content_request_common_enter_name_error_first_name_overlength_cy = \
            "Rydych wedi defnyddio gormod o nodau. Rhowch hyd at 35 o nodau"
        self.content_request_common_enter_name_error_last_name_cy = "Rhowch eich cyfenw"
        self.content_request_common_enter_name_error_last_name_overlength_cy = \
            "Rydych wedi defnyddio gormod o nodau. Rhowch hyd at 35 o nodau"

        self.content_request_code_sent_by_post_page_title_en = \
            '<title>Access code will be sent by post - ' + site_name_en + '</title>'
        self.content_request_code_hh_region_e_sent_post_title_en = \
            'A letter will be sent to Bob Bobbington at 1 Main Street, Upper Upperingham'
        self.content_request_code_hh_region_w_sent_post_title_en = \
            'A letter will be sent to Bob Bobbington at 1 West Street, West Westingham'
        self.content_request_code_aims_sent_post_title_en = \
            'A letter will be sent to Bob Bobbington at 1 Gate Reach, Exeter'
        self.content_request_code_sent_post_secondary_en = \
            'The letter with a new access code for you to start the study should arrive within 5 working days'
        self.content_request_code_sent_by_post_page_title_cy = \
            '<title>Access code will be sent by post - ' + site_name_cy + '</title>'
        self.content_request_code_hh_sent_post_title_cy = \
            'Caiff llythyr ei anfon at Bob Bobbington yn 1 West Street, West Westingham'
        self.content_request_code_aims_sent_post_title_cy = \
            'Caiff llythyr ei anfon at Bob Bobbington yn 1 Gate Reach, Exeter'
        self.content_request_code_sent_post_secondary_cy = \
            'The letter with a new access code for you to start the study should arrive within 5 working days'

        self.content_request_contact_centre_en = 'You need to call the Census customer contact centre'
        self.content_request_contact_centre_cy = "Mae angen i chi ffonio canolfan gyswllt cwsmeriaid y cyfrifiad"

        self.content_request_timeout_error_en = 're-enter your postcode'
        self.content_request_timeout_error_cy = 'nodi eich cod post eto'

        # Start Web Form

        self.get_webform_en = self.app.router['WebForm:get'].url_for(display_region='en')
        self.get_webform_cy = self.app.router['WebForm:get'].url_for(display_region='cy')
        self.post_webform_en = self.app.router['WebForm:post'].url_for(display_region='en')
        self.post_webform_cy = self.app.router['WebForm:post'].url_for(display_region='cy')

        self.webform_form_data = {
            'name': 'Bob Bobbington',
            'email': 'bob.bobbington@theinternet.co.uk',
            'description': 'Hello this is Bob',
            'category': 'MISSING_INFORMATION',
            'country': 'E'
        }

        self.rhsvc_url_web_form = (
            f'{rh_svc_url}/webform'
        )

        self.content_web_form_page_title_en = '<title>Web form - ' + site_name_en + '</title>'
        self.content_web_form_page_title_error_en = '<title>Error: Web form - ' + site_name_en + '</title>'
        self.content_web_form_title_en = 'Web form'
        self.content_web_form_warning_en = 'Information about what we do with your personal data is available in our'
        self.content_web_form_page_title_cy = '<title>Gwe-ffurflen - ' + site_name_cy + '</title>'
        self.content_web_form_page_title_error_cy = '<title>Gwall: Gwe-ffurflen - ' + site_name_cy + '</title>'
        self.content_web_form_title_cy = 'Gwe-ffurflen'
        self.content_web_form_warning_cy = \
            "Mae gwybodaeth am yr hyn rydym yn ei wneud gyda\\\'ch data personol ar gael yn ein"

        self.content_web_form_success_page_title_en = \
            '<title>Thank you for contacting us - ' + site_name_en + '</title>'
        self.content_web_form_success_title_en = 'Thank you for contacting us'
        self.content_web_form_success_confirmation_en = 'Your message has been sent'
        self.content_web_form_success_secondary_en = 'We will respond to you within 4 working days'
        self.content_web_form_success_page_title_cy = \
            '<title>Diolch am gysylltu \\xc3\\xa2 ni - ' + site_name_cy + '</title>'
        self.content_web_form_success_title_cy = 'Diolch am gysylltu \\xc3\\xa2 ni'
        self.content_web_form_success_confirmation_cy = "Mae eich neges wedi cael ei hanfon"
        self.content_web_form_success_secondary_cy = "Byddwn yn ymateb i chi o fewn 4 diwrnod gwaith"

        self.content_web_form_error_429_title_en = 'You have reached the maximum number web form submissions'
        self.content_web_form_error_429_title_cy = "Allwch chi ddim cyflwyno mwy o ffurflenni gwe"

        # Start Register
        self.get_register_en = self.app.router['Register:get'].url_for(display_region='en')

        # yapf: enable

    # URL functions
    def get_url_from_class(self, class_name, method_type, display_region=None, request_type=None):
        if display_region:
            if request_type:
                url = self.app.router[class_name + ':' + method_type].url_for(display_region=display_region,
                                                                              request_type=request_type)
            else:
                url = self.app.router[class_name + ':' + method_type].url_for(display_region=display_region)
        else:
            if request_type:
                url = self.app.router[class_name + ':' + method_type].url_for(request_type=request_type)
            else:
                url = self.app.router[class_name + ':' + method_type].url_for()
        return url
