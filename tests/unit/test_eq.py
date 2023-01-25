from unittest.mock import patch, Mock

from aiohttp import ClientResponseError
from aiohttp.web_exceptions import HTTPFound

from app.eq import EqLaunch
from app.exceptions import InvalidAccessCode, InactiveUacError, AlreadyReceiptedUacError
from app.rhsvc import RHSvc
from tests.unit.helpers import TestHelpers


class TestEq(TestHelpers):

    async def test_get_token(self):
        # Given
        app = {'DOMAIN_URL_PROTOCOL': 'http', 'DOMAIN_URL': 'domain_url', 'URL_PATH_PREFIX': 'url_prefix'}
        data = {'uac_hash': 'TEST_UAC_HASH'}

        expected_token = 'TEST_TOKEN'

        with patch.object(RHSvc, 'get_eq_launch_token', return_value='TEST_TOKEN') as rh_svc:
            rh_svc.get_eq_launch_token = expected_token
            # when
            actual_token = await EqLaunch.get_token(data, 'en', app)

            # then
            self.assertEqual(actual_token, expected_token)
            args = rh_svc.call_args.args
            self.assertEqual(args[0], data)
            self.assertEqual(args[1],
                             '/eqLaunch/TEST_UAC_HASH?accountServiceLogoutUrl=httpdomain_urlurl_prefix/en/signed-out'
                             '/&accountServiceUrl=httpdomain_urlurl_prefix/en/start/&languageCode=en')

    def test_call_eq(self):
        self.assertRaises(HTTPFound, EqLaunch.call_eq, 'eq_url_str', 'Test_token')

    async def test_inactive_access_code(self):
        # Given
        app_mock = {'DOMAIN_URL_PROTOCOL': 'http', 'DOMAIN_URL': 'domain_url', 'URL_PATH_PREFIX': 'url_prefix'}
        data = {'uac_hash': 'TEST_UAC_HASH', 'client_ip': 'xxx.xxx.xxx.xxx', 'client_id': 'clientId', 'trace': 'tracey'}

        client_response_error = ClientResponseError(status=400, message='UAC_INACTIVE', history=Mock(),
                                                    request_info=Mock())
        with patch.object(RHSvc, 'get_eq_launch_token') as patch_get_eq_launch_token:
            patch_get_eq_launch_token.side_effect = client_response_error

            expected_exception = None
            try:
                # when
                await EqLaunch.get_token(data, 'en', app_mock)
            except InactiveUacError as ex:
                expected_exception = ex

            self.assertEqual(type(expected_exception), InactiveUacError)

    async def test_already_receipted_code(self):
        # Given
        app_mock = {'DOMAIN_URL_PROTOCOL': 'http', 'DOMAIN_URL': 'domain_url', 'URL_PATH_PREFIX': 'url_prefix'}
        data = {'uac_hash': 'TEST_UAC_HASH', 'client_ip': 'xxx.xxx.xxx.xxx', 'client_id': 'clientId', 'trace': 'tracey'}

        client_response_error = ClientResponseError(status=400, message='UAC_RECEIPTED', history=Mock(),
                                                    request_info=Mock())
        with patch.object(RHSvc, 'get_eq_launch_token') as patch_get_eq_launch_token:
            patch_get_eq_launch_token.side_effect = client_response_error

            expected_exception = None

            try:
                # when
                await EqLaunch.get_token(data, 'en', app_mock)
            except AlreadyReceiptedUacError as ex:
                expected_exception = ex

            self.assertEqual(type(expected_exception), AlreadyReceiptedUacError)

    async def test_invalid_code_404_english(self):
        # Given
        app_mock = {'DOMAIN_URL_PROTOCOL': 'http', 'DOMAIN_URL': 'domain_url', 'URL_PATH_PREFIX': 'url_prefix'}
        data = {'uac_hash': 'TEST_UAC_HASH', 'client_ip': 'xxx.xxx.xxx.xxx', 'client_id': 'clientId', 'trace': 'tracey',
                'flash': []}

        client_response_error = ClientResponseError(status=404, history=Mock(), request_info=Mock())
        with patch.object(RHSvc, 'get_eq_launch_token') as patch_get_eq_launch_token:
            patch_get_eq_launch_token.side_effect = client_response_error

            expected_exception = None

            try:
                # when
                await EqLaunch.get_token(data, 'en', app_mock)
            except InvalidAccessCode as ex:
                expected_exception = ex

            self.assertEqual(type(expected_exception), InvalidAccessCode)
            # As part of code 'flash' has failure info attached to it, 'data' is a passed in and enriched, so we
            # can test it here
            self.assertEqual(data['flash'], [
                {'text': 'Access code not recognised. Enter the code again.', 'clickable': True, 'level': 'ERROR',
                 'type': 'INVALID_CODE', 'field': 'uac_invalid'}])

    async def test_invalid_code_404_welsh(self):
        # Given
        app_mock = {'DOMAIN_URL_PROTOCOL': 'http', 'DOMAIN_URL': 'domain_url', 'URL_PATH_PREFIX': 'url_prefix'}
        data = {'uac_hash': 'TEST_UAC_HASH', 'client_ip': 'xxx.xxx.xxx.xxx', 'client_id': 'clientId', 'trace': 'tracey',
                'flash': []}

        client_response_error = ClientResponseError(status=404, history=Mock(), request_info=Mock())
        with patch.object(RHSvc, 'get_eq_launch_token') as patch_get_eq_launch_token:
            patch_get_eq_launch_token.side_effect = client_response_error

            expected_exception = None

            try:
                # when
                await EqLaunch.get_token(data, 'cy', app_mock)
            except InvalidAccessCode as ex:
                expected_exception = ex

            self.assertEqual(type(expected_exception), InvalidAccessCode)
            # As part of code 'flash' has failure info attached to it, 'data' is a passed in and enriched, so we
            # can test it here
            self.assertEqual(data['flash'],
                             [{'text': 'Nid yw’r cod mynediad yn cael ei gydnabod. Rhowch y cod eto.',
                               'clickable': True, 'level': 'ERROR', 'type': 'INVALID_CODE', 'field': 'uac_invalid'}])
