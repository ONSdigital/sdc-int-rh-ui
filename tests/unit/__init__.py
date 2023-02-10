import asyncio
import json
import urllib.parse
import uuid
import functools

from aiohttp.test_utils import AioHTTPTestCase
from tenacity import wait_exponential

from app import app

from app import session, request
from aiohttp_session import session_middleware
from aiohttp_session import SimpleCookieStorage


def build_eq_raises(func, *args, **kwargs):
    """
    Helper decorator for manually patching the methods of app.eq.EqLaunch.

    This can be useful for tests that perform as a client but wish the server to raise InvalidForEqTokenGeneration
    when operations are called on an instance of app.eq.EqLaunch.

    The test case checks for and calls when possible .setUp and .tearDown attributes on each test method
    at server setUp (setUpAsync) and server tearDown (tearDownAsync).

    :param func: test method that requires the patch
    :param args: the test method's arguments
    :param args: the test method's keyword arguments
    :return: new method with patching functions attached as attributes
    """

    async def _override_eq_build_with_error(*_):
        from app import eq

        def init_replaced(*_):
            raise eq.InvalidForEqTokenGeneration('')

        eq.EqLaunch._bk__init__ = eq.EqLaunch.__init__
        eq.EqLaunch.__init__ = init_replaced

    async def _reset_eq_payload_constructor(*_):
        from app import eq

        eq.EqLaunch.__init__ = eq.EqLaunch._bk__init__

    @functools.wraps(func, *args, **kwargs)
    def new_func(self, *inner_args, **inner_kwargs):
        return func(self, *inner_args, **inner_kwargs)

    new_func.setUp = _override_eq_build_with_error
    new_func.tearDown = _reset_eq_payload_constructor

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
        await super().setUpAsync()
        test_method = getattr(self, self._testMethodName)
        if hasattr(test_method, 'setUp'):
            await test_method.setUp(self)

    async def tearDownAsync(self):
        await super().tearDownAsync()
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
            if event in record.message:
                all_matched = True

                for key, expected_value in kwargs.items():
                    try:
                        # The Url on the response now has encoded query params
                        if key == 'url':
                            encoded_url = record.__dict__[key]

                            split_url = encoded_url.split('?')
                            query_string_dict = urllib.parse.parse_qs(split_url[1])

                            actual_url = f'{urllib.parse.unquote(split_url[0])}?'

                            for query_key, query_value in query_string_dict.items():
                                decoded_value = urllib.parse.unquote(query_value[0])
                                actual_url = f'{actual_url}{query_key}={decoded_value}&'

                            actual_url = actual_url[:-1]

                            if actual_url == expected_value:
                                continue
                            else:
                                all_matched = False

                        if record.__dict__[key] == expected_value:
                            pass
                        else:
                            all_matched = False
                    except KeyError:
                        continue

                if all_matched:
                    return record

        self.fail(
            f"No matching log records with event: '{event}' and parameters: {kwargs},"
            f"{watcher.records}"
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
            error_prefix = 'PLACEHOLDER WELSH Error'
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
                panel_label_text = "PLACEHOLDER WELSH There is a problem with your answer"
            else:
                panel_label_text = "Mae problem gyda\\\'r dudalen hon"
        else:
            if panel_label == 'answer':
                panel_label_text = 'There is a problem with your answer'
            else:
                panel_label_text = 'There is a problem with this page'

        self.assertIn('<h2 id="alert" data-qa="error-header" class="ons-panel__title ons-u-fs-r--b">'
                      + panel_label_text + '</h2>', content)
        self.assertIn('<a href="#' + field_name + '" class="ons-list__link js-inpagelink">' + list_error + '</a>',
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

    def get_full_account_service_url(self, display_region):
        account_svc_url = self.app['ACCOUNT_SERVICE_URL']
        url_path_prefix = self.app['URL_PATH_PREFIX']
        return f'{account_svc_url}{url_path_prefix}/{display_region}/start/'

    async def asyncSetUp(self):
        # This section gets ugly if YAPF reformats it
        # yapf: disable
        await super().asyncSetUp()  # NB: setUp the server first so we can use self.app

        # URLs used in later statements
        rh_svc_url = self.app['RHSVC_URL']

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

        self.selected_uprn = '10023122451'

        self.mobile_valid = '07012345678'
        self.mobile_invalid_short = '07012'
        self.mobile_invalid_long = '0701234567890123456'
        self.mobile_invalid_character = '0701234567$'

        self.email_valid = 'test@testing.com'
        self.email_invalid = 'cheese.scone'

        self.field_empty = None

        self.common_form_data_empty = {}

        # Content
        self.content_call_centre_number_ew = '0800 141 2021'
        self.content_call_centre_number_cy = '0800 169 2021'

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

        self.content_common_429_error_eq_launch_title_cy = \
            "Rydym ni\\\'n brysur iawn ar hyn o bryd, diolch am eich amynedd"

        # End Common

        # Cookies
        self.content_cookies_page_title_en = '<title>Cookies on start.surveys.ons.gov.uk - ' + site_name_en + '</title>'
        self.content_cookies_page_title_cy = '<title>Cwcis ar start.surveys.ons.gov.uk - ' + site_name_cy + '</title>'

        self.content_cookies_heading_en = '<h1 class="ons-u-fs-xxl">Cookies on start.surveys.ons.gov.uk</h1>'
        self.content_cookies_heading_cy = '<h1 class="ons-u-fs-xxl">Cwcis ar start.surveys.ons.gov.uk</h1>'

        # Privacy and Data Protection
        self.content_privacy_page_title_en = '<title>Privacy and data protection - ' + site_name_en + '</title>'
        self.content_privacy_page_title_cy = '<title>Preifatrwydd a diogelu data - ' + \
                                             site_name_cy + '</title>'

        self.content_privacy_heading_en = '<h1 class="ons-u-fs-xl">Privacy and data protection</h1>'
        self.content_privacy_heading_cy = '<h1 class="ons-u-fs-xl">Preifatrwydd a diogelu data</h1>'

        # Start Journey

        # Content
        self.content_start_uac_already_used_en = 'This access code has already been used'
        self.content_start_uac_already_used_cy = "Mae\\\'r cod mynediad hwn eisoes wedi cael ei ddefnyddio"

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

        self.get_start_cy = self.app.router['Start:get'].url_for(display_region='cy')
        self.post_start_cy = self.app.router['Start:post'].url_for(display_region='cy')

        self.get_privacy_en = self.app.router['PrivacyAndDataProtection:get'].url_for(display_region='en')
        self.get_privacy_cy = self.app.router['PrivacyAndDataProtection:get'].url_for(display_region='cy')

        self.eq_id = '9999'
        self.form_type = 'zzz'
        self.jti = str(uuid.uuid4())
        self.uac_code = ''.join([str(n) for n in range(13)])
        self.uac1, self.uac2, self.uac3, self.uac4 = \
            self.uac_code[:4], self.uac_code[4:8], self.uac_code[8:12], self.uac_code[12:]
        self.period_id = '2021'
        self.uac = 'w4nwwpphjjptp7fn'
        self.uacHash = 'uacHashed'
        self.response_id = '111000000092a445af12905967d'
        self.questionnaire_id = '123424'
        self.channel = 'rh'

        self.eq_payload = {
            'no_point_in_this': 'until updated to new Token'
        }

        self.account_service_url = '/start/'

        self.rhsvc_url = (
            f'{rh_svc_url}/eqLaunch/{self.uacHash}'
        )

        self.start_data_valid = {
            'uac': self.uac, 'action[save_continue]': '',
        }

        self.content_common_error_panel_answer_en = 'There is a problem with your answer'
        self.content_common_error_panel_answer_cy = "Mae problem gyda\\\'ch ateb"
        self.content_common_error_select_an_option_en = 'Select an option'
        self.content_common_error_select_an_option_cy = 'Dewiswch opsiwn'

        f = asyncio.Future()
        f.set_result([])
        self.rhsvc_empty_array = f

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
