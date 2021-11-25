import json

from urllib.parse import urlsplit, parse_qs

from aiohttp.client_exceptions import ClientConnectionError
from aiohttp.test_utils import unittest_run_loop
from aioresponses import aioresponses

from app import (BAD_CODE_MSG, INVALID_CODE_MSG,
                 BAD_CODE_MSG_CY, INVALID_CODE_MSG_CY)
from app.exceptions import InactiveCaseError
from app.start_handlers import Start

from . import build_eq_raises, skip_encrypt

from .helpers import TestHelpers

attempts_retry_limit = 5


# noinspection PyTypeChecker
class TestStartHandlers(TestHelpers):
    user_journey = 'start'

    @unittest_run_loop
    async def test_post_start_with_retry_503_ew_e(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            self.mock503s(mocked, 2)
            mocked.get(self.rhsvc_url, payload=self.uac_json_e)

            response = await self.client.request('POST',
                                                 self.post_start_en,
                                                 allow_redirects=False,
                                                 data=self.start_data_valid)

        self.assertEqual(response.status, 302)
        self.assertIn('/en/start/confirm-address', response.headers['Location'])

    @unittest_run_loop
    async def test_post_start_with_retry_503_ew_w(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            self.mock503s(mocked, 2)
            mocked.get(self.rhsvc_url, payload=self.uac_json_w)

            response = await self.client.request('POST',
                                                 self.post_start_en,
                                                 allow_redirects=False,
                                                 data=self.start_data_valid)

        self.assertEqual(response.status, 302)
        self.assertIn('/en/start/confirm-address', response.headers['Location'])

    @unittest_run_loop
    async def test_post_start_with_retry_503_cy(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            self.mock503s(mocked, 2)
            mocked.get(self.rhsvc_url, payload=self.uac_json_w)

            response = await self.client.request('POST',
                                                 self.post_start_cy,
                                                 allow_redirects=False,
                                                 data=self.start_data_valid)

        self.assertEqual(response.status, 302)
        self.assertIn('/cy/start/confirm-address', response.headers['Location'])

    @unittest_run_loop
    async def test_post_start_with_retry_ConnectionError_ew_e(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url,
                       exception=ClientConnectionError('Failed'))
            mocked.get(self.rhsvc_url, payload=self.uac_json_e)

            response = await self.client.request('POST',
                                                 self.post_start_en,
                                                 allow_redirects=False,
                                                 data=self.start_data_valid)

        self.assertEqual(response.status, 302)
        self.assertIn('/en/start/confirm-address', response.headers['Location'])

    @unittest_run_loop
    async def test_post_start_with_retry_ConnectionError_ew_w(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url,
                       exception=ClientConnectionError('Failed'))
            mocked.get(self.rhsvc_url, payload=self.uac_json_w)

            response = await self.client.request('POST',
                                                 self.post_start_en,
                                                 allow_redirects=False,
                                                 data=self.start_data_valid)

        self.assertEqual(response.status, 302)
        self.assertIn('/en/start/confirm-address', response.headers['Location'])

    @unittest_run_loop
    async def test_post_start_with_retry_ConnectionError_cy(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url,
                       exception=ClientConnectionError('Failed'))
            mocked.get(self.rhsvc_url, payload=self.uac_json_w)

            response = await self.client.request('POST',
                                                 self.post_start_cy,
                                                 allow_redirects=False,
                                                 data=self.start_data_valid)

        self.assertEqual(response.status, 302)
        self.assertIn('/cy/start/confirm-address', response.headers['Location'])

    @build_eq_raises
    @unittest_run_loop
    async def test_post_start_build_raises_InvalidEqPayLoad_ew_e(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:

            mocked.get(self.rhsvc_url, payload=self.uac_json_e)
            mocked.post(self.rhsvc_url_surveylaunched)

            response = await self.client.request('POST',
                                                 self.post_start_en,
                                                 allow_redirects=False,
                                                 data=self.start_data_valid)
            self.assertEqual(response.status, 302)
            self.assertIn('/start/confirm-address',
                          response.headers['Location'])

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                # decorator makes URL constructor raise InvalidEqPayLoad when build() is called in handler
                response = await self.client.request(
                    'POST',
                    self.post_start_confirm_address_en,
                    allow_redirects=False,
                    data=self.start_confirm_address_data_yes)
            self.assertLogEvent(cm, 'service failed to build eq payload')

        # then error handler catches exception and renders error.html
        self.assert500Error(response, 'en', str(await response.content.read()), check_exit=True)

    @build_eq_raises
    @unittest_run_loop
    async def test_post_start_build_raises_InvalidEqPayLoad_ew_w(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json_w)
            mocked.post(self.rhsvc_url_surveylaunched)

            response = await self.client.request('POST',
                                                 self.post_start_en,
                                                 allow_redirects=False,
                                                 data=self.start_data_valid)
            self.assertEqual(response.status, 302)
            self.assertIn('/start/confirm-address',
                          response.headers['Location'])

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                # decorator makes URL constructor raise InvalidEqPayLoad when build() is called in handler
                response = await self.client.request(
                    'POST',
                    self.post_start_confirm_address_en,
                    allow_redirects=False,
                    data=self.start_confirm_address_data_yes)
            self.assertLogEvent(cm, 'service failed to build eq payload')

        # then error handler catches exception and renders error.html
        self.assert500Error(response, 'en', str(await response.content.read()), check_exit=True)

    @build_eq_raises
    @unittest_run_loop
    async def test_post_start_build_raises_InvalidEqPayLoad_cy(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json_w)
            mocked.post(self.rhsvc_url_surveylaunched)

            response = await self.client.request('POST',
                                                 self.post_start_cy,
                                                 allow_redirects=False,
                                                 data=self.start_data_valid)
            self.assertEqual(response.status, 302)
            self.assertIn('/cy/start/confirm-address/',
                          response.headers['Location'])

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                # decorator makes URL constructor raise InvalidEqPayLoad when build() is called in handler
                response = await self.client.request(
                    'POST',
                    self.post_start_confirm_address_cy,
                    allow_redirects=False,
                    data=self.start_confirm_address_data_yes)
            self.assertLogEvent(cm, 'service failed to build eq payload')

        # then error handler catches exception and renders error.html
        self.assert500Error(response, 'cy', str(await response.content.read()), check_exit=True)

    @unittest_run_loop
    async def test_post_start_invalid_blank_ew(self):
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
        self.assertIn('<a href="/cy/start/" lang="cy" >Cymraeg</a>', contents)
        self.assertMessagePanel(BAD_CODE_MSG, contents)

    @unittest_run_loop
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
        self.assertIn('<a href="/en/start/" lang="en" >English</a>', contents)
        self.assertMessagePanel(BAD_CODE_MSG_CY, contents)

    @unittest_run_loop
    async def test_post_start_invalid_text_url_ew(self):
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
        self.assertIn('<a href="/cy/start/" lang="cy" >Cymraeg</a>', contents)
        self.assertMessagePanel(INVALID_CODE_MSG, contents)

    @unittest_run_loop
    async def test_post_start_invalid_text_url_cy(self):
        form_data = self.start_data_valid.copy()
        form_data['uac'] = 'http://www.census.gov.uk/'

        with self.assertLogs('respondent-home', 'WARNING') as cm:
            response = await self.client.request('POST',
                                                 self.post_start_cy,
                                                 data=form_data)
        self.assertLogEvent(cm, 'attempt to use a malformed access code')

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertSiteLogo('cy', contents)
        self.assertIn('<a href="/en/start/" lang="en" >English</a>', contents)
        self.assertMessagePanel(INVALID_CODE_MSG_CY, contents)

    @unittest_run_loop
    async def test_post_start_invalid_text_random_ew(self):
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
        self.assertIn('<a href="/cy/start/" lang="cy" >Cymraeg</a>', contents)
        self.assertMessagePanel(INVALID_CODE_MSG, contents)

    @unittest_run_loop
    async def test_post_start_invalid_text_random_cy(self):
        form_data = self.start_data_valid.copy()
        form_data['uac'] = 'rT~l34u8{?nm4£#f'

        with self.assertLogs('respondent-home', 'WARNING') as cm:
            response = await self.client.request('POST',
                                                 self.post_start_cy,
                                                 data=form_data)
        self.assertLogEvent(cm, 'attempt to use a malformed access code')

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertSiteLogo('cy', contents)
        self.assertIn('<a href="/en/start/" lang="en" >English</a>', contents)
        self.assertMessagePanel(INVALID_CODE_MSG_CY, contents)

    @unittest_run_loop
    async def test_post_start_uac_closed_ew_e(self):
        uac_json = self.uac_json_e.copy()
        uac_json['active'] = False

        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=uac_json)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request('POST',
                                                     self.post_start_en,
                                                     data=self.start_data_valid)
            self.assertLogEvent(cm, 'attempt to access collection exercise that has already ended')

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertSiteLogo('en', contents)
        self.assertIn(self.content_start_closed_study, contents)

    @unittest_run_loop
    async def test_post_start_uac_closed_ew_w(self):
        uac_json = self.uac_json_w.copy()
        uac_json['active'] = False

        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=uac_json)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request('POST',
                                                     self.post_start_en,
                                                     data=self.start_data_valid)
            self.assertLogEvent(cm, 'attempt to access collection exercise that has already ended')

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertSiteLogo('en', contents)
        self.assertIn(self.content_start_closed_study, contents)

    @unittest_run_loop
    async def test_post_start_uac_closed_cy(self):
        uac_json = self.uac_json_w.copy()
        uac_json['active'] = False

        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=uac_json)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request('POST',
                                                     self.post_start_cy,
                                                     data=self.start_data_valid)
            self.assertLogEvent(cm, 'attempt to access collection exercise that has already ended')

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertSiteLogo('cy', contents)
        self.assertIn(self.content_start_closed_study, contents)

    @unittest_run_loop
    async def test_post_start_get_uac_connection_error_ew(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url,
                       exception=ClientConnectionError('Failed'))

            with self.assertLogs('respondent-home', 'WARN') as cm:
                response = await self.client.request('POST',
                                                     self.post_start_en,
                                                     data=self.start_data_valid)
            self.assertLogEvent(cm,
                                'client failed to connect',
                                url=self.rhsvc_url)

        self.assert500Error(response, 'en', str(await response.content.read()), check_exit=True)

    @unittest_run_loop
    async def test_post_start_get_uac_connection_error_cy(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url,
                       exception=ClientConnectionError('Failed'))

            with self.assertLogs('respondent-home', 'WARN') as cm:
                response = await self.client.request('POST',
                                                     self.post_start_cy,
                                                     data=self.start_data_valid)
            self.assertLogEvent(cm,
                                'client failed to connect',
                                url=self.rhsvc_url)

        self.assert500Error(response, 'cy', str(await response.content.read()), check_exit=True)

    async def should_use_default_error_handler(self, http_status):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, status=http_status)

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request('POST',
                                                     self.post_start_en,
                                                     data=self.start_data_valid)
            self.assertLogEvent(cm, 'response error', status=http_status, method="get", url=self.rhsvc_url)

        self.assertEqual(response.status, 500)

    @unittest_run_loop
    async def test_default_handler_4xx(self):
        status_list = [*range(400, 452)]
        status_list.remove(404)
        for st in status_list:
            await self.should_use_default_error_handler(st)

    @unittest_run_loop
    async def test_default_handler_5xx(self):
        status_list = [*range(500, 512)]
        status_list.remove(503)
        for st in status_list:
            await self.should_use_default_error_handler(st)

    async def assert_post_start_get_uac_error(self, display_region):
        await self.check_post_start_get_uac_error(
            self.get_url_from_class('Start', 'post', display_region, request_type=self.request_type),
            display_region, 500)
        await self.check_post_start_get_uac_error(
            self.get_url_from_class('Start', 'post', display_region, request_type=self.request_type),
            display_region, 403)
        await self.check_post_start_get_uac_error(
            self.get_url_from_class('Start', 'post', display_region, request_type=self.request_type),
            display_region, 400)
        await self.check_post_start_get_uac_error(
            self.get_url_from_class('Start', 'post', display_region, request_type=self.request_type),
            display_region, 401)

    @unittest_run_loop
    async def test_post_start_get_uac_error_ew(self):
        await self.assert_post_start_get_uac_error('en')

    @unittest_run_loop
    async def test_post_start_get_uac_error_cy(self):
        await self.assert_post_start_get_uac_error('cy')

    def mock503s(self, mocked, times):
        for i in range(times):
            mocked.get(self.rhsvc_url, status=503)

    @unittest_run_loop
    async def test_post_start_get_uac_503_ew(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            self.mock503s(mocked, attempts_retry_limit)

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request('POST',
                                                     self.post_start_en,
                                                     data=self.start_data_valid)
            self.assertLogEvent(cm, 'error in response', status_code=503)

        self.assert500Error(response, 'en', str(await response.content.read()), check_exit=True)

    @unittest_run_loop
    async def test_post_start_get_uac_503_cy(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            self.mock503s(mocked, attempts_retry_limit)

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request('POST',
                                                     self.post_start_cy,
                                                     data=self.start_data_valid)
            self.assertLogEvent(cm, 'error in response', status_code=503)

        self.assert500Error(response, 'cy', str(await response.content.read()), check_exit=True)

    @unittest_run_loop
    async def test_post_start_get_uac_404_ew(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, status=404)
            with self.assertLogs('respondent-home', 'WARN') as cm:
                response = await self.client.request('POST',
                                                     self.post_start_en,
                                                     data=self.start_data_valid)
            self.assertLogEvent(cm, 'attempt to use an invalid access code', client_ip=None)
        self.assertEqual(response.status, 401)
        self.assertLogEvent(cm, 'invalid access code entered')
        self.check_content_start('en', str(await response.content.read()), check_error=True)

    @unittest_run_loop
    async def test_post_start_get_uac_404_cy(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, status=404)
            with self.assertLogs('respondent-home', 'WARN') as cm:
                response = await self.client.request('POST',
                                                     self.post_start_cy,
                                                     data=self.start_data_valid)
            self.assertLogEvent(cm, 'attempt to use an invalid access code', client_ip=None)
        self.assertEqual(response.status, 401)
        self.assertLogEvent(cm, 'invalid access code entered')
        self.check_content_start('cy', str(await response.content.read()), check_error=True)

    @skip_encrypt
    @unittest_run_loop
    async def test_post_start_confirm_address_survey_launched_connection_error_ew_e(
            self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json_e)
            mocked.post(self.rhsvc_url_surveylaunched,
                        exception=ClientConnectionError('Failed'))

            response = await self.client.request('POST',
                                                 self.post_start_en,
                                                 data=self.start_data_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'WARN') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_start_confirm_address_en,
                    allow_redirects=False,
                    data=self.start_confirm_address_data_yes)
            self.assertLogEvent(cm,
                                'client failed to connect',
                                url=self.rhsvc_url_surveylaunched)

        self.assert500Error(response, 'en', str(await response.content.read()), check_exit=True)

    @skip_encrypt
    @unittest_run_loop
    async def test_post_start_confirm_address_survey_launched_connection_error_ew_w(
            self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json_w)
            mocked.post(self.rhsvc_url_surveylaunched,
                        exception=ClientConnectionError('Failed'))

            response = await self.client.request('POST',
                                                 self.post_start_en,
                                                 data=self.start_data_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'WARN') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_start_confirm_address_en,
                    allow_redirects=False,
                    data=self.start_confirm_address_data_yes)
            self.assertLogEvent(cm,
                                'client failed to connect',
                                url=self.rhsvc_url_surveylaunched)

        self.assert500Error(response, 'en', str(await response.content.read()), check_exit=True)

    @skip_encrypt
    @unittest_run_loop
    async def test_post_start_confirm_address_survey_launched_connection_error_cy(
            self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json_w)
            mocked.post(self.rhsvc_url_surveylaunched,
                        exception=ClientConnectionError('Failed'))

            response = await self.client.request('POST',
                                                 self.post_start_cy,
                                                 data=self.start_data_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'WARN') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_start_confirm_address_cy,
                    allow_redirects=False,
                    data=self.start_confirm_address_data_yes)
            self.assertLogEvent(cm,
                                'client failed to connect',
                                url=self.rhsvc_url_surveylaunched)

        self.assert500Error(response, 'cy', str(await response.content.read()), check_exit=True)

    async def assert_post_start_confirm_address_get_survey_launched_error(self, display_region, region):
        await self.check_post_start_confirm_address_get_survey_launched_error(
            self.get_url_from_class('Start', 'post', display_region, request_type=self.request_type),
            self.get_url_from_class('StartConfirmAddress', 'post', display_region, request_type=self.request_type),
            display_region, region, 401)
        await self.check_post_start_confirm_address_get_survey_launched_error(
            self.get_url_from_class('Start', 'post', display_region, request_type=self.request_type),
            self.get_url_from_class('StartConfirmAddress', 'post', display_region, request_type=self.request_type),
            display_region, region, 404)
        await self.check_post_start_confirm_address_get_survey_launched_error(
            self.get_url_from_class('Start', 'post', display_region, request_type=self.request_type),
            self.get_url_from_class('StartConfirmAddress', 'post', display_region, request_type=self.request_type),
            display_region, region, 500)
        await self.check_post_start_confirm_address_get_survey_launched_error(
            self.get_url_from_class('Start', 'post', display_region, request_type=self.request_type),
            self.get_url_from_class('StartConfirmAddress', 'post', display_region, request_type=self.request_type),
            display_region, region, 429)

    @unittest_run_loop
    async def test_post_start_confirm_address_get_survey_launched_error_ew_e(self):
        await self.assert_post_start_confirm_address_get_survey_launched_error('en', 'E')

    @unittest_run_loop
    async def test_post_start_confirm_address_get_survey_launched_error_ew_w(self):
        await self.assert_post_start_confirm_address_get_survey_launched_error('en', 'W')

    @unittest_run_loop
    async def test_post_start_confirm_address_get_survey_launched_error_cy(self):
        await self.assert_post_start_confirm_address_get_survey_launched_error('cy', 'W')

    def test_uac_hash(self):
        # Given some post data
        post_data = {'uac': 'w4nw wpph jjpt p7fn', 'action[save_continue]': ''}

        # When join_uac is called
        result = Start.uac_hash(post_data['uac'])

        # Then a single string built from the uac values is returned
        self.assertEqual(result, '54598f02da027026a584fd0bc7176de55a3e6472f4b3c74f68d0ae7be206e17c')

    def test_join_uac_missing(self):
        # Given some missing post data
        post_data = {'uac': '', 'action[save_continue]': ''}

        # When join_uac is called
        with self.assertRaises(TypeError):
            Start.uac_hash(post_data['uac'])
        # Then a TypeError is raised

    def test_join_uac_some_missing(self):
        # Given some missing post data
        post_data = {'uac': '123456781234', 'action[save_continue]': ''}

        # When join_uac is called
        with self.assertRaises(TypeError):
            Start.uac_hash(post_data['uac'])
        # Then a TypeError is raised

    def test_validate_case(self):
        # Given a dict with an active key and value
        case_json = {'active': True, 'caseStatus': 'OK'}

        # When validate_case is called
        Start.validate_case(case_json)

        # Nothing happens

    def test_validate_case_inactive(self):
        # Given a dict with an active key and value
        case_json = {'active': False, 'caseStatus': 'OK'}

        # When validate_case is called
        with self.assertRaises(InactiveCaseError):
            Start.validate_case(case_json)

        # Then an InactiveCaseError is raised

    def test_validate_case_empty(self):
        # Given an empty dict
        case_json = {}

        # When validate_case is called
        with self.assertRaises(InactiveCaseError):
            Start.validate_case(case_json)

        # Then an InactiveCaseError is raised

    @unittest_run_loop
    async def test_post_start_confirm_address_no_ew_e(self):
        display_region = 'en'
        with self.assertLogs('respondent-home', 'INFO') as cm, aioresponses(passthrough=[str(self.server._root)])\
                as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json_e)

            await self.client.request('GET', self.get_start_en)
            self.assertLogEvent(cm, "received GET on endpoint 'en/start'")

            await self.client.request('POST', self.post_start_en, allow_redirects=False, data=self.start_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/start'")

            response = await self.client.request('POST', self.post_start_confirm_address_en,
                                                 data=self.start_confirm_address_data_no)
            self.assertLogEvent(cm, "received POST on endpoint 'en/start/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/start/incorrect-address'")

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertSiteLogo(display_region, contents)
            self.assertIn('<a href="/cy/start/incorrect-address/" lang="cy" >Cymraeg</a>', contents)
            self.assertExitButton(display_region, contents)
            self.assertIn(self.content_start_incorrect_address_page_title_en, contents)
            self.assertIn(self.content_start_incorrect_address_title_en, contents)

    @unittest_run_loop
    async def test_post_start_confirm_address_no_ew_w(self):
        display_region = 'en'
        with self.assertLogs('respondent-home', 'INFO') as cm, aioresponses(passthrough=[str(self.server._root)])\
                as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json_w)

            await self.client.request('GET', self.get_start_en)
            self.assertLogEvent(cm, "received GET on endpoint 'en/start'")

            await self.client.request('POST', self.post_start_en, allow_redirects=False, data=self.start_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/start'")

            response = await self.client.request('POST', self.post_start_confirm_address_en,
                                                 data=self.start_confirm_address_data_no)
            self.assertLogEvent(cm, "received POST on endpoint 'en/start/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/start/incorrect-address'")

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertSiteLogo(display_region, contents)
            self.assertIn('<a href="/cy/start/incorrect-address/" lang="cy" >Cymraeg</a>', contents)
            self.assertExitButton(display_region, contents)
            self.assertIn(self.content_start_incorrect_address_page_title_en, contents)
            self.assertIn(self.content_start_incorrect_address_title_en, contents)

    @unittest_run_loop
    async def test_post_start_confirm_address_no_cy(self):
        display_region = 'cy'
        with self.assertLogs('respondent-home', 'INFO') as cm, aioresponses(passthrough=[str(self.server._root)])\
                as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json_w)

            await self.client.request('GET', self.get_start_cy)
            self.assertLogEvent(cm, "received GET on endpoint 'cy/start'")

            await self.client.request('POST', self.post_start_cy, allow_redirects=False, data=self.start_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/start'")

            response = await self.client.request('POST', self.post_start_confirm_address_cy,
                                                 data=self.start_confirm_address_data_no)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/start/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/start/incorrect-address'")

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertSiteLogo(display_region, contents)
            self.assertIn('<a href="/en/start/incorrect-address/" lang="en" >English</a>', contents)
            self.assertExitButton(display_region, contents)
            self.assertIn(self.content_start_incorrect_address_page_title_cy, contents)
            self.assertIn(self.content_start_incorrect_address_title_cy, contents)

    @unittest_run_loop
    async def test_post_start_confirm_address_empty_ew_e(self):
        display_region = 'en'
        with self.assertLogs('respondent-home', 'INFO') as cm, aioresponses(passthrough=[str(self.server._root)])\
                as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json_e)

            await self.client.request('GET', self.get_start_en)
            self.assertLogEvent(cm, "received GET on endpoint 'en/start'")

            await self.client.request('POST', self.post_start_en, allow_redirects=False, data=self.start_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/start'")

            response = await self.client.request('POST', self.post_start_confirm_address_en,
                                                 data=self.start_confirm_address_data_empty)
            self.assertLogEvent(cm, "received POST on endpoint 'en/start/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/start/confirm-address'")

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertSiteLogo(display_region, contents)
            self.assertIn('<a href="/cy/start/confirm-address/" lang="cy" >Cymraeg</a>', contents)
            self.assertExitButton(display_region, contents)
            self.assertIn(self.content_start_confirm_address_page_title_error_en, contents)
            self.assertIn(self.content_start_confirm_address_title_en, contents)
            self.assertIn(self.content_start_confirm_address_error_en, contents)

    @unittest_run_loop
    async def test_post_start_confirm_address_empty_ew_w(self):
        display_region = 'en'
        with self.assertLogs('respondent-home', 'INFO') as cm, aioresponses(passthrough=[str(self.server._root)])\
                as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json_w)

            await self.client.request('GET', self.get_start_en)
            self.assertLogEvent(cm, "received GET on endpoint 'en/start'")

            await self.client.request('POST', self.post_start_en, allow_redirects=False, data=self.start_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/start'")

            response = await self.client.request('POST', self.post_start_confirm_address_en,
                                                 data=self.start_confirm_address_data_empty)
            self.assertLogEvent(cm, "received POST on endpoint 'en/start/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/start/confirm-address'")

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertSiteLogo(display_region, contents)
            self.assertIn('<a href="/cy/start/confirm-address/" lang="cy" >Cymraeg</a>', contents)
            self.assertExitButton(display_region, contents)
            self.assertIn(self.content_start_confirm_address_page_title_error_en, contents)
            self.assertIn(self.content_start_confirm_address_title_en, contents)
            self.assertIn(self.content_start_confirm_address_error_en, contents)

    @unittest_run_loop
    async def test_post_start_confirm_address_empty_cy(self):
        display_region = 'cy'
        with self.assertLogs('respondent-home', 'INFO') as cm, aioresponses(passthrough=[str(self.server._root)])\
                as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json_w)

            await self.client.request('GET', self.get_start_cy)
            self.assertLogEvent(cm, "received GET on endpoint 'cy/start'")

            await self.client.request('POST', self.post_start_cy, allow_redirects=False, data=self.start_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/start'")

            response = await self.client.request('POST', self.post_start_confirm_address_cy,
                                                 data=self.start_confirm_address_data_empty)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/start/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/start/confirm-address'")

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertSiteLogo(display_region, contents)
            self.assertIn('<a href="/en/start/confirm-address/" lang="en" >English</a>', contents)
            self.assertExitButton(display_region, contents)
            self.assertIn(self.content_start_confirm_address_page_title_error_cy, contents)
            self.assertIn(self.content_start_confirm_address_title_cy, contents)
            self.assertIn(self.content_start_confirm_address_error_cy, contents)

    @unittest_run_loop
    async def test_post_start_confirm_address_invalid_ew_e(self):
        display_region = 'en'
        with self.assertLogs('respondent-home', 'INFO') as cm, aioresponses(passthrough=[str(self.server._root)])\
                as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json_e)

            await self.client.request('GET', self.get_start_en)
            self.assertLogEvent(cm, "received GET on endpoint 'en/start'")

            await self.client.request('POST', self.post_start_en, allow_redirects=False, data=self.start_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/start'")

            response = await self.client.request('POST', self.post_start_confirm_address_en,
                                                 data=self.start_confirm_address_data_invalid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/start/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/start/confirm-address'")

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertSiteLogo(display_region, contents)
            self.assertIn('<a href="/cy/start/confirm-address/" lang="cy" >Cymraeg</a>', contents)
            self.assertExitButton(display_region, contents)
            self.assertIn(self.content_start_confirm_address_page_title_error_en, contents)
            self.assertIn(self.content_start_confirm_address_title_en, contents)
            self.assertIn(self.content_start_confirm_address_error_en, contents)

    @unittest_run_loop
    async def test_post_start_confirm_address_invalid_ew_w(self):
        display_region = 'en'
        with self.assertLogs('respondent-home', 'INFO') as cm, aioresponses(passthrough=[str(self.server._root)])\
                as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json_w)

            await self.client.request('GET', self.get_start_en)
            self.assertLogEvent(cm, "received GET on endpoint 'en/start'")

            await self.client.request('POST', self.post_start_en, allow_redirects=False, data=self.start_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/start'")

            response = await self.client.request('POST', self.post_start_confirm_address_en,
                                                 data=self.start_confirm_address_data_invalid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/start/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/start/confirm-address'")

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertSiteLogo(display_region, contents)
            self.assertIn('<a href="/cy/start/confirm-address/" lang="cy" >Cymraeg</a>', contents)
            self.assertExitButton(display_region, contents)
            self.assertIn(self.content_start_confirm_address_page_title_error_en, contents)
            self.assertIn(self.content_start_confirm_address_title_en, contents)
            self.assertIn(self.content_start_confirm_address_error_en, contents)

    @unittest_run_loop
    async def test_post_start_confirm_address_invalid_cy(self):
        display_region = 'cy'
        with self.assertLogs('respondent-home', 'INFO') as cm, aioresponses(passthrough=[str(self.server._root)])\
                as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json_w)

            await self.client.request('GET', self.get_start_cy)
            self.assertLogEvent(cm, "received GET on endpoint 'cy/start'")

            await self.client.request('POST', self.post_start_cy, allow_redirects=False, data=self.start_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/start'")

            response = await self.client.request('POST', self.post_start_confirm_address_cy,
                                                 data=self.start_confirm_address_data_invalid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/start/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/start/confirm-address'")

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertSiteLogo(display_region, contents)
            self.assertIn('<a href="/en/start/confirm-address/" lang="en" >English</a>', contents)
            self.assertExitButton(display_region, contents)
            self.assertIn(self.content_start_confirm_address_page_title_error_cy, contents)
            self.assertIn(self.content_start_confirm_address_title_cy, contents)
            self.assertIn(self.content_start_confirm_address_error_cy, contents)

    @unittest_run_loop
    async def test_get_signed_out_ew(self):
        with self.assertLogs('respondent-home', 'INFO') as cm:
            response = await self.client.request('GET', self.get_signed_out_en)
            self.assertLogEvent(cm, "received GET on endpoint 'en/signed-out'")
            self.assertLogEvent(cm, "identity not previously remembered")
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.content_signed_out_page_title_en, contents)
            self.assertIn(self.content_signed_out_title_en, contents)
            self.assertSiteLogo('en', contents)
            self.assertIn('<a href="/cy/signed-out/" lang="cy" >Cymraeg</a>', contents)

    @unittest_run_loop
    async def test_get_signed_out_cy(self):
        with self.assertLogs('respondent-home', 'INFO') as cm:
            response = await self.client.request('GET', self.get_signed_out_cy)
            self.assertLogEvent(cm, "received GET on endpoint 'cy/signed-out'")
            self.assertLogEvent(cm, "identity not previously remembered")
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.content_signed_out_page_title_cy, contents)
            self.assertIn(self.content_signed_out_title_cy, contents)
            self.assertSiteLogo('cy', contents)
            self.assertIn('<a href="/en/signed-out/" lang="en" >English</a>', contents)

    @skip_encrypt
    @unittest_run_loop
    async def test_start_happy_path_ew_e(self):
        display_region = 'en'
        with self.assertLogs('respondent-home', 'INFO') as cm, aioresponses(
            passthrough=[str(self.server._root)]) \
                as mocked:

            mocked.get(self.rhsvc_url, payload=self.uac_json_e)

            mocked.post(self.rhsvc_url_surveylaunched)
            eq_payload = self.eq_payload.copy()
            eq_payload['region_code'] = 'GB-ENG'
            eq_payload['language_code'] = 'en'
            account_service_url = self.app['ACCOUNT_SERVICE_URL']
            url_path_prefix = self.app['URL_PATH_PREFIX']
            url_display_region = '/' + display_region
            eq_payload[
                'account_service_url'] = \
                f'{account_service_url}{url_path_prefix}{url_display_region}{self.account_service_url}'
            eq_payload[
                'account_service_log_out_url'] = \
                f'{account_service_url}{url_path_prefix}{url_display_region}{self.account_service_log_out_url}'
            eq_payload['ru_ref'] = '11100000009'
            eq_payload['display_address'] = 'ONS, Segensworth Road'

            get_start_response = await self.client.request('GET', self.get_start_en)
            self.assertEqual(200, get_start_response.status)
            self.assertLogEvent(cm, "received GET on endpoint 'en/start'")
            self.check_content_start(display_region, str(await get_start_response.content.read()))

            post_start_response = await self.client.request('POST',
                                                            self.post_start_en,
                                                            allow_redirects=True,
                                                            data=self.start_data_valid)

            self.assertLogEvent(cm, "received POST on endpoint 'en/start'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/start/confirm-address'")

            self.assertEqual(200, post_start_response.status)
            confirm_address_content = str(await post_start_response.content.read())
            self.assertSiteLogo(display_region, confirm_address_content)
            self.assertIn('<a href="/cy/start/confirm-address/" lang="cy" >Cymraeg</a>', confirm_address_content)
            self.assertExitButton(display_region, confirm_address_content)
            self.assertIn(self.content_start_confirm_address_page_title_en, confirm_address_content)
            self.assertIn(self.content_start_confirm_address_title_en, confirm_address_content)
            self.assertIn(self.content_start_confirm_address_option_yes_en, confirm_address_content)
            self.assertIn(self.content_start_confirm_address_option_no_en, confirm_address_content)

            post_confirm_address_response = await self.client.request(
                'POST',
                self.post_start_confirm_address_en,
                allow_redirects=False,
                data=self.start_confirm_address_data_yes)

            self.assertLogEvent(cm, 'redirecting to eq')

        self.assertEqual(post_confirm_address_response.status, 302)
        redirected_url = post_confirm_address_response.headers['location']
        # outputs url on fail
        self.assertTrue(redirected_url.startswith(self.app['EQ_URL']),
                        redirected_url)
        # we only care about the query string
        _, _, _, query, *_ = urlsplit(redirected_url)
        # convert token to dict
        token = json.loads(parse_qs(query)['token'][0])
        # fail early if payload keys differ
        self.assertEqual(eq_payload.keys(), token.keys())
        for key in eq_payload.keys():
            # skip uuid / time generated values
            if key in ['jti', 'tx_id', 'iat', 'exp']:
                continue
            # outputs failed key as msg
            self.assertEqual(eq_payload[key], token[key], key)

    @skip_encrypt
    @unittest_run_loop
    async def test_start_happy_path_ew_w(self):
        display_region = 'en'
        with self.assertLogs('respondent-home', 'INFO') as cm, aioresponses(
            passthrough=[str(self.server._root)]) \
                as mocked:

            mocked.get(self.rhsvc_url, payload=self.uac_json_w)

            mocked.post(self.rhsvc_url_surveylaunched)
            eq_payload = self.eq_payload.copy()
            eq_payload['region_code'] = 'GB-WLS'
            eq_payload['language_code'] = 'en'
            account_service_url = self.app['ACCOUNT_SERVICE_URL']
            url_path_prefix = self.app['URL_PATH_PREFIX']
            url_display_region = '/' + display_region
            eq_payload[
                'account_service_url'] = \
                f'{account_service_url}{url_path_prefix}{url_display_region}{self.account_service_url}'
            eq_payload[
                'account_service_log_out_url'] = \
                f'{account_service_url}{url_path_prefix}{url_display_region}{self.account_service_log_out_url}'
            eq_payload['ru_ref'] = '11100000009'
            eq_payload['display_address'] = 'ONS, Segensworth Road'

            get_start_response = await self.client.request('GET', self.get_start_en)
            self.assertEqual(200, get_start_response.status)
            self.assertLogEvent(cm, "received GET on endpoint 'en/start'")
            self.check_content_start(display_region, str(await get_start_response.content.read()))

            post_start_response = await self.client.request('POST',
                                                            self.post_start_en,
                                                            allow_redirects=True,
                                                            data=self.start_data_valid)

            self.assertLogEvent(cm, "received POST on endpoint 'en/start'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/start/confirm-address'")

            self.assertEqual(200, post_start_response.status)
            confirm_address_content = str(await post_start_response.content.read())
            self.assertSiteLogo(display_region, confirm_address_content)
            self.assertIn('<a href="/cy/start/confirm-address/" lang="cy" >Cymraeg</a>', confirm_address_content)
            self.assertExitButton(display_region, confirm_address_content)
            self.assertIn(self.content_start_confirm_address_page_title_en, confirm_address_content)
            self.assertIn(self.content_start_confirm_address_title_en, confirm_address_content)
            self.assertIn(self.content_start_confirm_address_option_yes_en, confirm_address_content)
            self.assertIn(self.content_start_confirm_address_option_no_en, confirm_address_content)

            post_confirm_address_response = await self.client.request(
                'POST',
                self.post_start_confirm_address_en,
                allow_redirects=False,
                data=self.start_confirm_address_data_yes)

            self.assertLogEvent(cm, 'redirecting to eq')

        self.assertEqual(post_confirm_address_response.status, 302)
        redirected_url = post_confirm_address_response.headers['location']
        # outputs url on fail
        self.assertTrue(redirected_url.startswith(self.app['EQ_URL']),
                        redirected_url)
        # we only care about the query string
        _, _, _, query, *_ = urlsplit(redirected_url)
        # convert token to dict
        token = json.loads(parse_qs(query)['token'][0])
        # fail early if payload keys differ
        self.assertEqual(eq_payload.keys(), token.keys())
        for key in eq_payload.keys():
            # skip uuid / time generated values
            if key in ['jti', 'tx_id', 'iat', 'exp']:
                continue
            # outputs failed key as msg
            self.assertEqual(eq_payload[key], token[key], key)

    @skip_encrypt
    @unittest_run_loop
    async def test_start_happy_path_cy(self):
        display_region = 'cy'
        with self.assertLogs('respondent-home', 'INFO') as cm, aioresponses(
            passthrough=[str(self.server._root)]) \
                as mocked:

            mocked.get(self.rhsvc_url, payload=self.uac_json_w)

            mocked.post(self.rhsvc_url_surveylaunched)
            eq_payload = self.eq_payload.copy()
            eq_payload['region_code'] = 'GB-WLS'
            eq_payload['language_code'] = 'cy'
            account_service_url = self.app['ACCOUNT_SERVICE_URL']
            url_path_prefix = self.app['URL_PATH_PREFIX']
            url_display_region = '/' + display_region
            eq_payload[
                'account_service_url'] = \
                f'{account_service_url}{url_path_prefix}{url_display_region}{self.account_service_url}'
            eq_payload[
                'account_service_log_out_url'] = \
                f'{account_service_url}{url_path_prefix}{url_display_region}{self.account_service_log_out_url}'
            eq_payload['ru_ref'] = '11100000009'
            eq_payload['display_address'] = 'ONS, Segensworth Road'

            get_start_response = await self.client.request('GET', self.get_start_cy)
            self.assertEqual(200, get_start_response.status)
            self.assertLogEvent(cm, "received GET on endpoint 'cy/start'")
            self.check_content_start(display_region, str(await get_start_response.content.read()))

            post_start_response = await self.client.request('POST',
                                                            self.post_start_cy,
                                                            allow_redirects=True,
                                                            data=self.start_data_valid)

            self.assertLogEvent(cm, "received POST on endpoint 'cy/start'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/start/confirm-address'")

            self.assertEqual(200, post_start_response.status)
            confirm_address_content = str(await post_start_response.content.read())
            self.assertSiteLogo(display_region, confirm_address_content)
            self.assertIn('<a href="/en/start/confirm-address/" lang="en" >English</a>', confirm_address_content)
            self.assertExitButton(display_region, confirm_address_content)
            self.assertIn(self.content_start_confirm_address_page_title_cy, confirm_address_content)
            self.assertIn(self.content_start_confirm_address_title_cy, confirm_address_content)
            self.assertIn(self.content_start_confirm_address_option_yes_cy, confirm_address_content)
            self.assertIn(self.content_start_confirm_address_option_no_cy, confirm_address_content)

            post_confirm_address_response = await self.client.request(
                'POST',
                self.post_start_confirm_address_cy,
                allow_redirects=False,
                data=self.start_confirm_address_data_yes)

            self.assertLogEvent(cm, 'redirecting to eq')

        self.assertEqual(post_confirm_address_response.status, 302)
        redirected_url = post_confirm_address_response.headers['location']
        # outputs url on fail
        self.assertTrue(redirected_url.startswith(self.app['EQ_URL']),
                        redirected_url)
        # we only care about the query string
        _, _, _, query, *_ = urlsplit(redirected_url)
        # convert token to dict
        token = json.loads(parse_qs(query)['token'][0])
        # fail early if payload keys differ
        self.assertEqual(eq_payload.keys(), token.keys())
        for key in eq_payload.keys():
            # skip uuid / time generated values
            if key in ['jti', 'tx_id', 'iat', 'exp']:
                continue
            # outputs failed key as msg
            self.assertEqual(eq_payload[key], token[key], key)

    @unittest_run_loop
    async def test_post_start_for_receiptReceived_true_ew_e(self):
        uac_json = self.uac_json_e.copy()
        uac_json['receiptReceived'] = True
        with self.assertLogs('respondent-home', 'WARNING') as cm, aioresponses(
                passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=uac_json)

            response = await self.client.request('POST',
                                                 self.post_start_en,
                                                 data=self.start_data_valid)

            self.assertLogEvent(cm, "attempt to use an inactive access code")
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertSiteLogo('en', contents)
            self.assertIn(self.content_start_uac_already_used_en, contents)

    @unittest_run_loop
    async def test_post_start_for_receiptReceived_true_cy(self):
        uac_json = self.uac_json_w.copy()
        uac_json['receiptReceived'] = True
        with self.assertLogs('respondent-home', 'WARNING') as cm, aioresponses(
                passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=uac_json)

            response = await self.client.request('POST',
                                                 self.post_start_cy,
                                                 data=self.start_data_valid)

            self.assertLogEvent(cm, "attempt to use an inactive access code")
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertSiteLogo('cy', contents)
            self.assertIn(self.content_start_uac_already_used_cy, contents)
