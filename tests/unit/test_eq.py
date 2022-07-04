from unittest import mock
from unittest.mock import patch, MagicMock, Mock

from aiohttp import ClientResponseError, RequestInfo, ClientResponse
from aiohttp.web_exceptions import HTTPFound

from app.eq import EqLaunch
from app.exceptions import InvalidForEqTokenGeneration, InvalidAccessCode

from aiohttp.web import Application

from app.rhsvc import RHSvc
from tests.utilities.test_case_helper import test_helper


class TestEq:
    async def test_get_token(self):
        # Given
        app = {'DOMAIN_URL_PROTOCOL': 'http', 'DOMAIN_URL_EN': 'domain_url', 'URL_PATH_PREFIX': 'url_prefix'}
        data = {'uac_hash': 'TEST_UAC_HASH'}

        expected_token = 'TEST_TOKEN'

        with patch.object(RHSvc, 'get_eq_launch_token', return_value='TEST_TOKEN') as rh_svc:
            rh_svc.get_eq_launch_token = expected_token
            # when
            actual_token = await EqLaunch.get_token(data, 'en', app)

            # then
            test_helper.assertEqual(actual_token, expected_token)
            args = rh_svc.call_args.args
            test_helper.assertEqual(args[0], data)
            test_helper.assertEqual(args[1],
                                    '/eqLaunch/TEST_UAC_HASH?languageCode=en&accountServiceUrl'
                                    '=httpdomain_urlurl_prefix/en/start/&accountServiceLogoutUrl'
                                    '=httpdomain_urlurl_prefix/en/signed-out/')

    def test_call_eq(self):
        test_helper.assertRaises(HTTPFound, EqLaunch.call_eq, 'eq_url_str', 'Test_token')

    # TODO: test throwing exception work
    # async def test_invalid_access_code(selfs):
    #     # request_info = RequestInfo()
    #     # history = Tuple[ClientResponse, ...]
    #     # client_response_error = ClientResponseError(request_info=request_info, history=)
    #     #
    #     # request_info: RequestInfo,
    #     # history: Tuple[ClientResponse, ...],
    #     # *,
    #     # code: Optional[int] = None,
    #     # status: Optiona
    #     # client_response_error.status = 404
    #
    #     rc = MagicMock
    #     history = Mock
    #
    #     client_response_error = ClientResponseError(request_info=rc, history=history)
    #
    #     mock_res.status = 400
    #     mock_conn.getresponse = MagicMock(return_value=mock_res)
    #
    #     app_mock = {'DOMAIN_URL_PROTOCOL': 'http', 'DOMAIN_URL_EN': 'domain_url', 'URL_PATH_PREFIX': 'url_prefix'}
    #     data = {'uac_hash': 'TEST_UAC_HASH'}
    #
    #     with patch.object(RHSvc, 'get_eq_launch_token', client_response_error):
    #         # when
    #         test_helper.assertRaises(InvalidAccessCode, await EqLaunch.get_token(data, 'en', app_mock))
