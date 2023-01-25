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

    def mock_ai_503s(self, mocked, times):
        for i in range(times):
            mocked.get(self.addressindexsvc_url + self.postcode_valid + '?limit=' + self.aims_postcode_limit,
                       status=503)

    async def check_get_timeout(self, url, display_region):
        with self.assertLogs('respondent-home', 'INFO') as cm:

            response = await self.client.request('GET', url)
            self.assertLogEvent(cm, self.build_url_log_entry('timeout', display_region, 'GET'))
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertSiteLogo(display_region, contents)

            self.assertCorrectTranslationLink(contents, display_region, self.user_journey, self.request_type, 'timeout')

            if display_region == 'cy':
                self.assertIn(self.content_common_timeout_cy, contents)
                self.assertIn(self.content_request_timeout_error_cy, contents)
            else:
                self.assertIn(self.content_common_timeout_en, contents)
                self.assertIn(self.content_request_timeout_error_en, contents)

    def check_content_start(self, display_region, contents, check_empty=False, check_error=False):
        if display_region == 'cy':
            title_tag = 'PLACEHOLDER WELSH Start study'
            h1_title = 'PLACEHOLDER WELSH Start study'
            secondary_text = "PLACEHOLDER WELSH Enter your 16-character access code"
            error_text_link = "Nid yw\\'r cod mynediad yn cael ei gydnabod. Rhowch y cod eto."
            error_text = error_text_link
            error_text_empty = 'PLACEHOLDER WELSH Enter an access code'
        else:
            title_tag = 'Start study'
            h1_title = 'Start study'
            secondary_text = 'Enter your 16-character access code'
            error_text_link = 'Access code not recognised. Enter the code again.'
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
            response = await self.client.request('GET',
                                                 self.get_url_from_class('Start', 'get', display_region))
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
