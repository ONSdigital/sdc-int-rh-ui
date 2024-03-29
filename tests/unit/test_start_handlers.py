from aiohttp.client_exceptions import ClientConnectionError
from aioresponses import aioresponses

from app.constants import BAD_CODE_MSG, INVALID_CODE_MSG, BAD_CODE_LENGTH_MSG, BAD_CODE_LENGTH_MSG_CY, BAD_CODE_MSG_CY
from app.start_handlers import Start
from .helpers import TestHelpers

attempts_retry_limit = 5


# noinspection PyTypeChecker
class TestStartHandlers(TestHelpers):
    user_journey = 'start'
    eq_launch_url_en = 'http://localhost:8071/eqLaunch' \
                       '/54598f02da027026a584fd0bc7176de55a3e6472f4b3c74f68d0ae7be206e17c' \
                       '?accountServiceUrl=http://localhost:9092&languageCode=en'

    eq_launch_url_cy = 'http://localhost:8071/eqLaunch' \
                       '/54598f02da027026a584fd0bc7176de55a3e6472f4b3c74f68d0ae7be206e17c' \
                       '?accountServiceUrl=http://localhost:9092&languageCode=cy'

    async def test_post_start_invalid_blank_en(self):
        form_data = self.start_data_valid.copy()
        form_data['uac'] = ''

        with self.assertLogs('respondent-home', 'INFO') as cm:
            response = await self.client.request('POST',
                                                 self.post_start_en,
                                                 data=form_data)
        self.assertLogEvent(cm, 'access code not supplied')

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertSiteLogo('en', contents)
        self.assertCorrectTranslationLink(contents, 'en', self.user_journey)
        self.assertMessagePanel(BAD_CODE_MSG, contents)

    async def test_post_start_invalid_blank_cy(self):
        form_data = self.start_data_valid.copy()
        form_data['uac'] = ''

        with self.assertLogs('respondent-home', 'INFO') as cm:
            response = await self.client.request('POST',
                                                 self.post_start_cy,
                                                 data=form_data)
        self.assertLogEvent(cm, 'access code not supplied')

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertSiteLogo('cy', contents)
        self.assertCorrectTranslationLink(contents, 'cy', self.user_journey)
        self.assertMessagePanel(BAD_CODE_MSG_CY, contents)

    async def test_post_start_invalid_length_en(self):
        form_data = self.start_data_valid.copy()
        form_data['uac'] = '1'

        with self.assertLogs('respondent-home', 'INFO') as cm:
            response = await self.client.request('POST',
                                                 self.post_start_en,
                                                 data=form_data)
        self.assertLogEvent(cm, 'attempt to use a malformed access code')

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertSiteLogo('en', contents)
        self.assertCorrectTranslationLink(contents, 'en', self.user_journey)
        self.assertMessagePanel(BAD_CODE_LENGTH_MSG, contents)

    async def test_post_start_invalid_length_cy(self):
        form_data = self.start_data_valid.copy()
        form_data['uac'] = '1'

        with self.assertLogs('respondent-home', 'INFO') as cm:
            response = await self.client.request('POST',
                                                 self.post_start_cy,
                                                 data=form_data)
        self.assertLogEvent(cm, 'attempt to use a malformed access code')

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertSiteLogo('cy', contents)
        self.assertCorrectTranslationLink(contents, 'cy', self.user_journey)
        self.assertMessagePanel(BAD_CODE_LENGTH_MSG_CY, contents)

    async def test_post_start_invalid_text_url_en(self):
        form_data = self.start_data_valid.copy()
        form_data['uac'] = 'http://www.census.gov.uk/'

        with self.assertLogs('respondent-home', 'WARNING') as cm:
            response = await self.client.request('POST',
                                                 self.post_start_en,
                                                 data=form_data)
        self.assertLogEvent(cm, 'attempt to use a malformed access code')

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertSiteLogo('en', contents)
        self.assertCorrectTranslationLink(contents, 'en', self.user_journey)
        self.assertMessagePanel(INVALID_CODE_MSG, contents)

    async def test_post_start_invalid_text_random_en(self):
        form_data = self.start_data_valid.copy()
        form_data['uac'] = 'rT~l34u8{?nm4£#f'

        with self.assertLogs('respondent-home', 'WARNING') as cm:
            response = await self.client.request('POST',
                                                 self.post_start_en,
                                                 data=form_data)
        self.assertLogEvent(cm, 'attempt to use a malformed access code')

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertSiteLogo('en', contents)
        self.assertCorrectTranslationLink(contents, 'en', self.user_journey)
        self.assertMessagePanel(INVALID_CODE_MSG, contents)

    async def test_post_start_uac_closed_en(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.eq_launch_url_en, status=400, body="UAC_INACTIVE")

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request('POST',
                                                     self.post_start_en,
                                                     data=self.start_data_valid)
            self.assertLogEvent(cm, 'attempt to use inactive UAC')

        self.assertEqual(200, response.status)
        contents = str(await response.content.read())
        self.assertSiteLogo('en', contents)
        self.assertIn("This questionnaire has now closed", contents)

    async def test_post_start_get_uac_connection_error_ew(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.eq_launch_url_en,
                       exception=ClientConnectionError('Failed'))

            with self.assertLogs('respondent-home', 'WARN') as cm:
                response = await self.client.request('POST',
                                                     self.post_start_en,
                                                     data=self.start_data_valid)
            self.assertLogEvent(cm,
                                'client failed to connect',
                                url=self.eq_launch_url_en)

        self.assert500Error(response, 'en', str(await response.content.read()), check_exit=True)

    async def should_use_default_error_handler(self, http_status):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.eq_launch_url_en, status=http_status)

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request('POST',
                                                     self.post_start_en,
                                                     data=self.start_data_valid)
            self.assertLogEvent(cm, 'response error', status=http_status, method="get", url=self.eq_launch_url_en)

        self.assertEqual(response.status, 500)

    async def test_default_handler_4xx(self):
        status_list = [*range(400, 452)]
        status_list.remove(404)
        status_list.remove(429)

        for st in status_list:
            await self.should_use_default_error_handler(st)

    async def test_default_handler_5xx(self):
        status_list = [*range(500, 512)]
        status_list.remove(503)
        status_list = [500]
        for st in status_list:
            await self.should_use_default_error_handler(st)

    async def test_post_start_get_uac_404_en(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.eq_launch_url_en, status=404)
            with self.assertLogs('respondent-home', 'WARN') as cm:
                response = await self.client.request('POST',
                                                     self.post_start_en,
                                                     data=self.start_data_valid)
            self.assertLogEvent(cm, 'attempt to use an invalid access code', client_ip=None)
        self.assertEqual(401, response.status)
        self.assertLogEvent(cm, 'invalid access code entered')
        self.check_content_start('en', str(await response.content.read()), check_error=True)

    async def test_post_start_get_uac_404_cy(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.eq_launch_url_cy, status=404)
            with self.assertLogs('respondent-home', 'WARN') as cm:
                response = await self.client.request('POST',
                                                     self.post_start_cy,
                                                     data=self.start_data_valid)
            self.assertLogEvent(cm, 'attempt to use an invalid access code', client_ip=None)
        self.assertEqual(response.status, 401)
        self.assertLogEvent(cm, 'invalid access code entered')
        self.check_content_start('cy', str(await response.content.read()), check_error=True)

    def test_uac_hash(self):
        # Given
        uac = 'W4NWWPPHJJPTP7FN'

        # When join_uac is called
        result = Start._uac_hash(uac)

        # Then a single string built from the uac values is returned
        self.assertEqual(result, '54598f02da027026a584fd0bc7176de55a3e6472f4b3c74f68d0ae7be206e17c')

    def test_join_uac_missing(self):
        # Given some missing post data
        uac = ''

        # When join_uac is called
        with self.assertRaises(TypeError):
            Start._uac_hash(uac)
        # Then a TypeError is raised

    def test_join_uac_some_missing(self):
        # Given
        uac = '123456781234'

        # When join_uac is called
        with self.assertRaises(TypeError):
            Start._uac_hash(uac)
        # Then a TypeError is raised

    async def test_post_start_for_receipt_received_true_en(self):
        with self.assertLogs('respondent-home', 'WARNING') as cm, aioresponses(
                passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.eq_launch_url_en, body='UAC_RECEIPTED', status=400)

            response = await self.client.request('POST',
                                                 self.post_start_en,
                                                 data=self.start_data_valid)

            self.assertLogEvent(cm, "attempt to use receipted UAC")
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertSiteLogo('en', contents)
            self.assertIn(self.content_start_uac_already_used_en, contents)
            self.assertIn(self.content_breadcrumbs_back_button_en, contents)
            self.assertCorrectTranslationLink(contents, 'en', self.user_journey)

    async def test_post_start_for_receipt_received_true_cy(self):
        with self.assertLogs('respondent-home', 'WARNING') as cm, aioresponses(
                passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.eq_launch_url_cy, body='UAC_RECEIPTED', status=400)

            response = await self.client.request('POST',
                                                 self.post_start_cy,
                                                 data=self.start_data_valid)

            self.assertLogEvent(cm, "attempt to use receipted UAC")
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertSiteLogo('cy', contents)
            self.assertIn(self.content_start_uac_already_used_cy, contents)
            self.assertIn(self.content_breadcrumbs_back_button_cy, contents)
            self.assertCorrectTranslationLink(contents, 'cy', self.user_journey)

    async def test_post_start_for_receipt_deactivated_en(self):
        with self.assertLogs('respondent-home', 'WARNING') as cm, aioresponses(
                passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.eq_launch_url_en, body='UAC_INACTIVE', status=400)

            response = await self.client.request('POST',
                                                 self.post_start_en,
                                                 data=self.start_data_valid)

            self.assertLogEvent(cm, "attempt to use inactive UAC")
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertSiteLogo('en', contents)
            self.assertIn(self.content_start_uac_deactivated_en, contents)
            self.assertIn(self.content_breadcrumbs_back_button_en, contents)
            self.assertCorrectTranslationLink(contents, 'en', self.user_journey)

    async def test_post_start_for_receipt_deactivated_cy(self):
        with self.assertLogs('respondent-home', 'WARNING') as cm, aioresponses(
                passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.eq_launch_url_cy, body='UAC_INACTIVE', status=400)

            response = await self.client.request('POST',
                                                 self.post_start_cy,
                                                 data=self.start_data_valid)

            self.assertLogEvent(cm, "attempt to use inactive UAC")
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertSiteLogo('cy', contents)
            self.assertIn(self.content_start_uac_deactivated_cy, contents)
            self.assertIn(self.content_breadcrumbs_back_button_cy, contents)
            self.assertCorrectTranslationLink(contents, 'cy', self.user_journey)
