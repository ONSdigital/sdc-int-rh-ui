import json

from urllib.parse import urlsplit, parse_qs

from aiohttp.client_exceptions import ClientConnectionError
from aiohttp.test_utils import unittest_run_loop
from aioresponses import aioresponses

from app import (BAD_CODE_MSG, INVALID_CODE_MSG,
                 BAD_CODE_MSG_CY, INVALID_CODE_MSG_CY)
from app.exceptions import InactiveCaseError, InvalidEqPayLoad
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
        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertIn(self.content_common_500_error_en, contents)

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
        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertIn(self.content_common_500_error_en, contents)

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
        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.content_common_500_error_cy, contents)
        self.assertIn(self.ons_logo_cy, contents)

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
        self.assertIn(self.ons_logo_en, contents)
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
        self.assertIn(self.ons_logo_cy, contents)
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
        self.assertIn(self.ons_logo_en, contents)
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
        self.assertIn(self.ons_logo_cy, contents)
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
        self.assertIn(self.ons_logo_en, contents)
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
        self.assertIn(self.ons_logo_cy, contents)
        self.assertIn('<a href="/en/start/" lang="en" >English</a>', contents)
        self.assertMessagePanel(INVALID_CODE_MSG_CY, contents)

    @unittest_run_loop
    async def test_post_start_uac_active_missing_ew_e(self):
        uac_json = self.uac_json_e.copy()
        del uac_json['active']

        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=uac_json)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request('POST',
                                                     self.post_start_en,
                                                     data=self.start_data_valid)
            self.assertLogEvent(cm, 'attempt to use an inactive access code')

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertIn(self.content_start_uac_expired_en, contents)

    @unittest_run_loop
    async def test_post_start_uac_active_missing_ew_w(self):
        uac_json = self.uac_json_w.copy()
        del uac_json['active']

        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=uac_json)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request('POST',
                                                     self.post_start_en,
                                                     data=self.start_data_valid)
            self.assertLogEvent(cm, 'attempt to use an inactive access code')

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertIn(self.content_start_uac_expired_en, contents)

    @unittest_run_loop
    async def test_post_start_uac_active_missing_cy(self):
        uac_json = self.uac_json_w.copy()
        del uac_json['active']

        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=uac_json)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request('POST',
                                                     self.post_start_cy,
                                                     data=self.start_data_valid)
            self.assertLogEvent(cm, 'attempt to use an inactive access code')

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_cy, contents)
        self.assertIn(self.content_start_uac_expired_cy, contents)

    @unittest_run_loop
    async def test_post_start_uac_inactive_ew_e(self):
        uac_json = self.uac_json_e.copy()
        uac_json['active'] = False

        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=uac_json)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request('POST',
                                                     self.post_start_en,
                                                     data=self.start_data_valid)
            self.assertLogEvent(cm, 'attempt to use an inactive access code')

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertIn(self.content_start_uac_expired_en, contents)

    @unittest_run_loop
    async def test_post_start_uac_inactive_ew_w(self):
        uac_json = self.uac_json_w.copy()
        uac_json['active'] = False

        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=uac_json)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request('POST',
                                                     self.post_start_en,
                                                     data=self.start_data_valid)
            self.assertLogEvent(cm, 'attempt to use an inactive access code')

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertIn(self.content_start_uac_expired_en, contents)

    @unittest_run_loop
    async def test_post_start_uac_inactive_cy(self):
        uac_json = self.uac_json_w.copy()
        uac_json['active'] = False

        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=uac_json)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request('POST',
                                                     self.post_start_cy,
                                                     data=self.start_data_valid)
            self.assertLogEvent(cm, 'attempt to use an inactive access code')

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_cy, contents)
        self.assertIn(self.content_start_uac_expired_cy, contents)

    @unittest_run_loop
    async def test_post_start_uac_case_status_not_found_ew_e(self):
        uac_json = self.uac_json_e.copy()
        uac_json['caseStatus'] = 'NOT_FOUND'

        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=uac_json)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request('POST',
                                                     self.post_start_en,
                                                     data=self.start_data_valid)
            self.assertLogEvent(cm, 'service failed to build eq payload')

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_post_start_uac_case_status_not_found_ew_w(self):
        uac_json = self.uac_json_w.copy()
        uac_json['caseStatus'] = 'NOT_FOUND'

        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=uac_json)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request('POST',
                                                     self.post_start_en,
                                                     data=self.start_data_valid)
            self.assertLogEvent(cm, 'service failed to build eq payload')

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_post_start_uac_case_status_not_found_cy(self):
        uac_json = self.uac_json_w.copy()
        uac_json['caseStatus'] = 'NOT_FOUND'

        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=uac_json)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request('POST',
                                                     self.post_start_cy,
                                                     data=self.start_data_valid)
            self.assertLogEvent(cm, 'service failed to build eq payload')

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.content_common_500_error_cy, contents)
        self.assertIn(self.ons_logo_cy, contents)

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

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertIn(self.content_common_500_error_en, contents)

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

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.content_common_500_error_cy, contents)
        self.assertIn(self.ons_logo_cy, contents)

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

    @unittest_run_loop
    async def test_post_start_get_uac_500_ew(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, status=500)

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request('POST',
                                                     self.post_start_en,
                                                     data=self.start_data_valid)
            self.assertLogEvent(cm, 'error in response', status_code=500)
            self.assertLogEvent(cm, 'response error')

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_post_start_get_uac_500_cy(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, status=500)

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request('POST',
                                                     self.post_start_cy,
                                                     data=self.start_data_valid)
            self.assertLogEvent(cm, 'error in response', status_code=500)

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.content_common_500_error_cy, contents)
        self.assertIn(self.ons_logo_cy, contents)

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

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_post_start_get_uac_503_cy(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            self.mock503s(mocked, attempts_retry_limit)

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request('POST',
                                                     self.post_start_cy,
                                                     data=self.start_data_valid)
            self.assertLogEvent(cm, 'error in response', status_code=503)

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.content_common_500_error_cy, contents)
        self.assertIn(self.ons_logo_cy, contents)

    @unittest_run_loop
    async def test_post_start_get_uac_404_ew(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, status=404)

            with self.assertLogs('respondent-home', 'WARN') as cm:
                response = await self.client.request('POST',
                                                     self.post_start_en,
                                                     data=self.start_data_valid)
            self.assertLogEvent(cm,
                                'attempt to use an invalid access code',
                                client_ip=None)

        self.assertEqual(response.status, 401)
        self.assertLogEvent(cm, 'invalid access code entered')
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertIn(self.content_start_page_title_error_en, contents)
        self.assertIn('<a href="/cy/start/" lang="cy" >Cymraeg</a>', contents)
        self.assertMessagePanel(INVALID_CODE_MSG, contents)

    @unittest_run_loop
    async def test_post_start_get_uac_404_cy(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, status=404)

            with self.assertLogs('respondent-home', 'WARN') as cm:
                response = await self.client.request('POST',
                                                     self.post_start_cy,
                                                     data=self.start_data_valid)
            self.assertLogEvent(cm,
                                'attempt to use an invalid access code',
                                client_ip=None)

        self.assertEqual(response.status, 401)
        self.assertLogEvent(cm, 'invalid access code entered')
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_cy, contents)
        self.assertIn(self.content_start_page_title_error_cy, contents)
        self.assertIn('<a href="/en/start/" lang="en" >English</a>', contents)
        self.assertMessagePanel(INVALID_CODE_MSG_CY, contents)

    @unittest_run_loop
    async def test_post_start_get_uac_403_ew(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, status=403)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request('POST',
                                                     self.post_start_en,
                                                     data=self.start_data_valid)
            self.assertLogEvent(cm, 'error in response', status_code=403)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_post_start_get_uac_403_cy(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, status=403)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request('POST',
                                                     self.post_start_cy,
                                                     data=self.start_data_valid)
            self.assertLogEvent(cm, 'error in response', status_code=403)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.content_common_500_error_cy, contents)
            self.assertIn(self.ons_logo_cy, contents)

    @unittest_run_loop
    async def test_post_start_get_uac_401_ew(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, status=401)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request('POST',
                                                     self.post_start_en,
                                                     data=self.start_data_valid)
            self.assertLogEvent(cm, 'error in response', status_code=401)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_post_start_get_uac_401_cy(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, status=401)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request('POST',
                                                     self.post_start_cy,
                                                     data=self.start_data_valid)
            self.assertLogEvent(cm, 'error in response', status_code=401)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.content_common_500_error_cy, contents)
            self.assertIn(self.ons_logo_cy, contents)

    @unittest_run_loop
    async def test_post_start_get_uac_400_ew(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, status=400)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request('POST',
                                                     self.post_start_en,
                                                     data=self.start_data_valid)
            self.assertLogEvent(cm, 'bad request', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_post_start_get_uac_400_cy(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, status=400)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request('POST',
                                                     self.post_start_cy,
                                                     data=self.start_data_valid)
            self.assertLogEvent(cm, 'bad request', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.content_common_500_error_cy, contents)
            self.assertIn(self.ons_logo_cy, contents)

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

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertIn(self.content_common_500_error_en, contents)

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

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertIn(self.content_common_500_error_en, contents)

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

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.content_common_500_error_cy, contents)
        self.assertIn(self.ons_logo_cy, contents)

    @unittest_run_loop
    async def test_post_start_confirm_address_get_survey_launched_401_ew_e(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json_e)
            mocked.post(self.rhsvc_url_surveylaunched, status=401)

            response = await self.client.request('POST',
                                                 self.post_start_en,
                                                 data=self.start_data_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_start_confirm_address_en,
                    allow_redirects=False,
                    data=self.start_confirm_address_data_yes)
            self.assertLogEvent(cm, 'error in response', status_code=401)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_post_start_confirm_address_get_survey_launched_401_ew_w(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json_w)
            mocked.post(self.rhsvc_url_surveylaunched, status=401)

            response = await self.client.request('POST',
                                                 self.post_start_en,
                                                 data=self.start_data_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_start_confirm_address_en,
                    allow_redirects=False,
                    data=self.start_confirm_address_data_yes)
            self.assertLogEvent(cm, 'error in response', status_code=401)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_post_start_confirm_address_get_survey_launched_401_cy(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json_w)
            mocked.post(self.rhsvc_url_surveylaunched, status=401)

            response = await self.client.request('POST',
                                                 self.post_start_cy,
                                                 data=self.start_data_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_start_confirm_address_cy,
                    allow_redirects=False,
                    data=self.start_confirm_address_data_yes)
            self.assertLogEvent(cm, 'error in response', status_code=401)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.content_common_500_error_cy, contents)
            self.assertIn(self.ons_logo_cy, contents)

    @unittest_run_loop
    async def test_post_address_confirmation_get_survey_launched_404_ew_e(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json_e)
            mocked.post(self.rhsvc_url_surveylaunched, status=404)

            response = await self.client.request('POST',
                                                 self.post_start_en,
                                                 data=self.start_data_valid)
            self.assertEqual(response.status, 200)

            response = await self.client.request(
                'POST',
                self.post_start_confirm_address_en,
                allow_redirects=False,
                data=self.start_confirm_address_data_yes)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_post_address_confirmation_get_survey_launched_404_ew_w(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json_w)
            mocked.post(self.rhsvc_url_surveylaunched, status=404)

            response = await self.client.request('POST',
                                                 self.post_start_en,
                                                 data=self.start_data_valid)
            self.assertEqual(response.status, 200)

            response = await self.client.request(
                'POST',
                self.post_start_confirm_address_en,
                allow_redirects=False,
                data=self.start_confirm_address_data_yes)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_post_start_confirm_address_get_survey_launched_404_cy(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json_w)
            mocked.post(self.rhsvc_url_surveylaunched, status=404)

            response = await self.client.request('POST',
                                                 self.post_start_cy,
                                                 data=self.start_data_valid)
            self.assertEqual(response.status, 200)

            response = await self.client.request(
                'POST',
                self.post_start_confirm_address_cy,
                allow_redirects=False,
                data=self.start_confirm_address_data_yes)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.content_common_500_error_cy, contents)
            self.assertIn(self.ons_logo_cy, contents)

    @unittest_run_loop
    async def test_post_start_confirm_address_get_survey_launched_500_ew_e(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json_e)
            mocked.post(self.rhsvc_url_surveylaunched, status=500)

            response = await self.client.request('POST',
                                                 self.post_start_en,
                                                 data=self.start_data_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_start_confirm_address_en,
                    allow_redirects=False,
                    data=self.start_confirm_address_data_yes)
            self.assertLogEvent(cm, 'error in response', status_code=500)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_post_start_confirm_address_get_survey_launched_500_ew_w(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json_w)
            mocked.post(self.rhsvc_url_surveylaunched, status=500)

            response = await self.client.request('POST',
                                                 self.post_start_en,
                                                 data=self.start_data_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_start_confirm_address_en,
                    allow_redirects=False,
                    data=self.start_confirm_address_data_yes)
            self.assertLogEvent(cm, 'error in response', status_code=500)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_post_start_confirm_address_get_survey_launched_500_cy(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json_w)
            mocked.post(self.rhsvc_url_surveylaunched, status=500)

            response = await self.client.request('POST',
                                                 self.post_start_cy,
                                                 data=self.start_data_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_start_confirm_address_cy,
                    allow_redirects=False,
                    data=self.start_confirm_address_data_yes)
            self.assertLogEvent(cm, 'error in response', status_code=500)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.content_common_500_error_cy, contents)
            self.assertIn(self.ons_logo_cy, contents)

    @unittest_run_loop
    async def test_post_start_confirm_address_get_survey_launched_429_ew_e(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json_e)
            mocked.post(self.rhsvc_url_surveylaunched, status=429)

            response = await self.client.request('POST',
                                                 self.post_start_en,
                                                 data=self.start_data_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_start_confirm_address_en,
                    allow_redirects=False,
                    data=self.start_confirm_address_data_yes)
            self.assertLogEvent(cm, 'too many requests', status_code=429)
            self.assertLogEvent(cm, 'session invalidated')
            self.assertEqual(response.status, 429)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_common_429_error_eq_launch_title_en, contents)
            self.assertNotIn(self.content_start_exit_button_en, contents)

    @unittest_run_loop
    async def test_post_start_confirm_address_get_survey_launched_429_ew_w(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json_w)
            mocked.post(self.rhsvc_url_surveylaunched, status=429)

            response = await self.client.request('POST',
                                                 self.post_start_en,
                                                 data=self.start_data_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_start_confirm_address_en,
                    allow_redirects=False,
                    data=self.start_confirm_address_data_yes)
            self.assertLogEvent(cm, 'too many requests', status_code=429)
            self.assertLogEvent(cm, 'session invalidated')
            self.assertEqual(response.status, 429)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_common_429_error_eq_launch_title_en, contents)
            self.assertNotIn(self.content_start_exit_button_en, contents)

    @unittest_run_loop
    async def test_post_start_confirm_address_get_survey_launched_429_cy(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.rhsvc_url, payload=self.uac_json_w)
            mocked.post(self.rhsvc_url_surveylaunched, status=429)

            response = await self.client.request('POST',
                                                 self.post_start_cy,
                                                 data=self.start_data_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_start_confirm_address_cy,
                    allow_redirects=False,
                    data=self.start_confirm_address_data_yes)
            self.assertLogEvent(cm, 'too many requests', status_code=429)
            self.assertLogEvent(cm, 'session invalidated')
            self.assertEqual(response.status, 429)
            contents = str(await response.content.read())
            self.assertIn(self.content_common_429_error_eq_launch_title_cy, contents)
            self.assertIn(self.ons_logo_cy, contents)
            self.assertNotIn(self.content_start_exit_button_cy, contents)

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

    def test_validate_caseStatus_notfound(self):
        # Given a dict with an active key and value
        case_json = {'active': True, 'caseStatus': 'NOT_FOUND'}

        # When validate_case is called
        with self.assertRaises(InvalidEqPayLoad):
            Start.validate_case(case_json)

        # Then an InvalidEqPayload is raised

    def test_validate_case_empty(self):
        # Given an empty dict
        case_json = {}

        # When validate_case is called
        with self.assertRaises(InactiveCaseError):
            Start.validate_case(case_json)

        # Then an InactiveCaseError is raised

    @unittest_run_loop
    async def test_post_start_confirm_address_empty_ew_e(self):
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
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn('<a href="/cy/start/confirm-address/" lang="cy" >Cymraeg</a>', contents)
            self.assertIn(self.content_start_exit_button_en, contents)
            self.assertIn(self.content_start_confirm_address_page_title_error_en, contents)
            self.assertIn(self.content_start_confirm_address_title_en, contents)
            self.assertIn(self.content_start_confirm_address_error_en, contents)

    @unittest_run_loop
    async def test_post_start_confirm_address_empty_ew_w(self):
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
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn('<a href="/cy/start/confirm-address/" lang="cy" >Cymraeg</a>', contents)
            self.assertIn(self.content_start_exit_button_en, contents)
            self.assertIn(self.content_start_confirm_address_page_title_error_en, contents)
            self.assertIn(self.content_start_confirm_address_title_en, contents)
            self.assertIn(self.content_start_confirm_address_error_en, contents)

    @unittest_run_loop
    async def test_post_start_confirm_address_empty_cy(self):
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
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn('<a href="/en/start/confirm-address/" lang="en" >English</a>', contents)
            self.assertIn(self.content_start_exit_button_cy, contents)
            self.assertIn(self.content_start_confirm_address_page_title_error_cy, contents)
            self.assertIn(self.content_start_confirm_address_title_cy, contents)
            self.assertIn(self.content_start_confirm_address_error_cy, contents)

    @unittest_run_loop
    async def test_post_start_confirm_address_invalid_ew_e(self):
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
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn('<a href="/cy/start/confirm-address/" lang="cy" >Cymraeg</a>', contents)
            self.assertIn(self.content_start_exit_button_en, contents)
            self.assertIn(self.content_start_confirm_address_page_title_error_en, contents)
            self.assertIn(self.content_start_confirm_address_title_en, contents)
            self.assertIn(self.content_start_confirm_address_error_en, contents)

    @unittest_run_loop
    async def test_post_start_confirm_address_invalid_ew_w(self):
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
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn('<a href="/cy/start/confirm-address/" lang="cy" >Cymraeg</a>', contents)
            self.assertIn(self.content_start_exit_button_en, contents)
            self.assertIn(self.content_start_confirm_address_page_title_error_en, contents)
            self.assertIn(self.content_start_confirm_address_title_en, contents)
            self.assertIn(self.content_start_confirm_address_error_en, contents)

    @unittest_run_loop
    async def test_post_start_confirm_address_invalid_cy(self):
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
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn('<a href="/en/start/confirm-address/" lang="en" >English</a>', contents)
            self.assertIn(self.content_start_exit_button_cy, contents)
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
            self.assertIn(self.ons_logo_en, contents)
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
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn('<a href="/en/signed-out/" lang="en" >English</a>', contents)

    @skip_encrypt
    @unittest_run_loop
    async def test_start_happy_path_ew_e(self):
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
            url_display_region = '/en'
            eq_payload[
                'account_service_url'] = \
                f'{account_service_url}{url_path_prefix}{url_display_region}{self.account_service_url}'
            eq_payload[
                'account_service_log_out_url'] = \
                f'{account_service_url}{url_path_prefix}{url_display_region}{self.account_service_log_out_url}'
            eq_payload['ru_ref'] = 'xxxxxxxxxxx'
            eq_payload['display_address'] = 'ONS, Segensworth Road'

            get_start_response = await self.client.request('GET', self.get_start_en)
            self.assertEqual(200, get_start_response.status)
            self.assertLogEvent(cm, "received GET on endpoint 'en/start'")
            start_contents = str(await get_start_response.content.read())
            self.assertIn(self.ons_logo_en, start_contents)
            self.assertIn('<a href="/cy/start/" lang="cy" >Cymraeg</a>', start_contents)
            self.assertIn(self.content_start_title_en, start_contents)
            self.assertIn(self.content_start_uac_title_en, start_contents)
            self.assertEqual(start_contents.count('input--text'), 1)
            self.assertIn('type="submit"', start_contents)

            post_start_response = await self.client.request('POST',
                                                            self.post_start_en,
                                                            allow_redirects=True,
                                                            data=self.start_data_valid)

            self.assertLogEvent(cm, "received POST on endpoint 'en/start'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/start/confirm-address'")

            self.assertEqual(200, post_start_response.status)
            confirm_address_content = str(await post_start_response.content.read())
            self.assertIn(self.ons_logo_en, confirm_address_content)
            self.assertIn('<a href="/cy/start/confirm-address/" lang="cy" >Cymraeg</a>', confirm_address_content)
            self.assertIn(self.content_start_exit_button_en, confirm_address_content)
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
            url_display_region = '/en'
            eq_payload[
                'account_service_url'] = \
                f'{account_service_url}{url_path_prefix}{url_display_region}{self.account_service_url}'
            eq_payload[
                'account_service_log_out_url'] = \
                f'{account_service_url}{url_path_prefix}{url_display_region}{self.account_service_log_out_url}'
            eq_payload['ru_ref'] = 'xxxxxxxxxxx'
            eq_payload['display_address'] = 'ONS, Segensworth Road'

            get_start_response = await self.client.request('GET', self.get_start_en)
            self.assertEqual(200, get_start_response.status)
            self.assertLogEvent(cm, "received GET on endpoint 'en/start'")
            start_contents = str(await get_start_response.content.read())
            self.assertIn(self.ons_logo_en, start_contents)
            self.assertIn('<a href="/cy/start/" lang="cy" >Cymraeg</a>', start_contents)
            self.assertIn(self.content_start_title_en, start_contents)
            self.assertIn(self.content_start_uac_title_en, start_contents)
            self.assertEqual(start_contents.count('input--text'), 1)
            self.assertIn('type="submit"', start_contents)

            post_start_response = await self.client.request('POST',
                                                            self.post_start_en,
                                                            allow_redirects=True,
                                                            data=self.start_data_valid)

            self.assertLogEvent(cm, "received POST on endpoint 'en/start'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/start/confirm-address'")

            self.assertEqual(200, post_start_response.status)
            confirm_address_content = str(await post_start_response.content.read())
            self.assertIn(self.ons_logo_en, confirm_address_content)
            self.assertIn('<a href="/cy/start/confirm-address/" lang="cy" >Cymraeg</a>', confirm_address_content)
            self.assertIn(self.content_start_exit_button_en, confirm_address_content)
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
            url_display_region = '/cy'
            eq_payload[
                'account_service_url'] = \
                f'{account_service_url}{url_path_prefix}{url_display_region}{self.account_service_url}'
            eq_payload[
                'account_service_log_out_url'] = \
                f'{account_service_url}{url_path_prefix}{url_display_region}{self.account_service_log_out_url}'
            eq_payload['ru_ref'] = 'xxxxxxxxxxx'
            eq_payload['display_address'] = 'ONS, Segensworth Road'

            get_start_response = await self.client.request('GET', self.get_start_cy)
            self.assertEqual(200, get_start_response.status)
            self.assertLogEvent(cm, "received GET on endpoint 'cy/start'")
            start_contents = str(await get_start_response.content.read())
            self.assertIn(self.ons_logo_cy, start_contents)
            self.assertIn('<a href="/en/start/" lang="en" >English</a>', start_contents)
            self.assertIn(self.content_start_title_cy, start_contents)
            self.assertIn(self.content_start_uac_title_cy, start_contents)
            self.assertEqual(start_contents.count('input--text'), 1)
            self.assertIn('type="submit"', start_contents)

            post_start_response = await self.client.request('POST',
                                                            self.post_start_cy,
                                                            allow_redirects=True,
                                                            data=self.start_data_valid)

            self.assertLogEvent(cm, "received POST on endpoint 'cy/start'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/start/confirm-address'")

            self.assertEqual(200, post_start_response.status)
            confirm_address_content = str(await post_start_response.content.read())
            self.assertIn(self.ons_logo_cy, confirm_address_content)
            self.assertIn('<a href="/en/start/confirm-address/" lang="en" >English</a>', confirm_address_content)
            self.assertIn(self.content_start_exit_button_cy, confirm_address_content)
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
