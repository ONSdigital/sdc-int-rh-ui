from aiohttp.test_utils import unittest_run_loop
from .helpers import TestHelpers


# noinspection PyTypeChecker
class TestRequestHandlersAccessCode(TestHelpers):

    user_journey = 'request'
    request_type = 'access-code'

    async def assert_request_access_code_sms_happy_path(self, display_region, region):
        await self.check_get_enter_address(display_region)
        await self.check_post_enter_address(display_region)
        await self.check_post_select_address(display_region, region)
        await self.check_post_confirm_address_input_yes_code(display_region)
        await self.check_post_select_how_to_receive_input_sms(display_region)
        await self.check_post_enter_mobile(display_region)
        await self.check_post_confirm_send_by_text(display_region, region)

    async def assert_post_request_access_code_enter_address_no_results(self, display_region):
        await self.check_get_enter_address(display_region)
        await self.check_post_enter_address_input_returns_no_results(display_region)

    async def assert_post_request_access_code_get_ai_postcode_error(self, display_region):
        await self.check_post_enter_address_error_from_ai(
            self.get_url_from_class('RequestEnterAddress', 'get', display_region, request_type=self.request_type),
            self.get_url_from_class('RequestEnterAddress', 'post', display_region, request_type=self.request_type),
            display_region, 500)
        await self.check_post_enter_address_error_503_from_ai(
            self.get_url_from_class('RequestEnterAddress', 'post', display_region, request_type=self.request_type),
            display_region)
        await self.check_post_enter_address_error_from_ai(
            self.get_url_from_class('RequestEnterAddress', 'get', display_region, request_type=self.request_type),
            self.get_url_from_class('RequestEnterAddress', 'post', display_region, request_type=self.request_type),
            display_region, 403)
        await self.check_post_enter_address_error_from_ai(
            self.get_url_from_class('RequestEnterAddress', 'get', display_region, request_type=self.request_type),
            self.get_url_from_class('RequestEnterAddress', 'post', display_region, request_type=self.request_type),
            display_region, 401)
        await self.check_post_enter_address_error_from_ai(
            self.get_url_from_class('RequestEnterAddress', 'get', display_region, request_type=self.request_type),
            self.get_url_from_class('RequestEnterAddress', 'post', display_region, request_type=self.request_type),
            display_region, 400)
        await self.check_post_enter_address_error_from_ai(
            self.get_url_from_class('RequestEnterAddress', 'get', display_region, request_type=self.request_type),
            self.get_url_from_class('RequestEnterAddress', 'post', display_region, request_type=self.request_type),
            display_region, 429)
        await self.check_post_enter_address_connection_error_from_ai(
            self.get_url_from_class('RequestEnterAddress', 'post', display_region, request_type=self.request_type),
            display_region)
        await self.check_post_enter_address_connection_error_from_ai(
            self.get_url_from_class('RequestEnterAddress', 'post', display_region, request_type=self.request_type),
            display_region, epoch='test')

    async def assert_get_request_access_code_address_not_found(self, display_region):
        await self.check_get_enter_address(display_region)
        await self.check_post_enter_address(display_region)
        await self.check_post_select_address_address_not_found(display_region)

    async def assert_post_request_access_code_enter_address_empty(self, display_region):
        await self.check_get_enter_address(display_region)
        await self.check_post_enter_address_input_empty(display_region)

    async def assert_post_request_access_code_enter_address_invalid_postcode(self, display_region):
        await self.check_get_enter_address(display_region)
        await self.check_post_enter_address_input_invalid(display_region)

    async def assert_get_request_access_code_confirm_address_get_cases_error(self, display_region):
        await self.check_get_enter_address(display_region)
        await self.check_post_enter_address(display_region)
        await self.check_post_select_address_error_from_get_cases(display_region)

    async def assert_get_request_access_code_enter_address_finder(self, display_region, region):
        await self.check_get_enter_address(display_region)
        await self.check_post_enter_address_finder(display_region, region)

    async def assert_get_request_access_code_confirm_address_data_no(self, display_region, region):
        await self.check_get_enter_address(display_region)
        await self.check_post_enter_address(display_region)
        await self.check_post_select_address(display_region, region)
        await self.check_post_confirm_address_input_no(display_region)

    async def assert_get_request_access_code_confirm_address_data_invalid(self, display_region, region):
        await self.check_get_enter_address(display_region)
        await self.check_post_enter_address(display_region)
        await self.check_post_select_address(display_region, region)
        await self.check_post_confirm_address_input_invalid(display_region)

    async def assert_get_request_access_code_confirm_address_data_no_selection(self, display_region, region):
        await self.check_get_enter_address(display_region)
        await self.check_post_enter_address(display_region)
        await self.check_post_select_address(display_region, region)
        await self.check_post_confirm_address_input_no_selection(display_region)

    async def assert_post_request_access_code_select_address_no_selection(self, display_region):
        await self.check_get_enter_address(display_region)
        await self.check_post_enter_address(display_region)
        await self.check_post_select_address_no_selection_made(display_region)

    async def assert_post_request_access_code_select_address_no_case(self, display_region):
        await self.check_get_enter_address(display_region)
        await self.check_post_enter_address(display_region)
        await self.check_post_select_address_no_case(display_region)

    async def assert_post_request_access_code_select_how_to_receive_no_selection(self, display_region, region):
        await self.check_get_enter_address(display_region)
        await self.check_post_enter_address(display_region)
        await self.check_post_select_address(display_region, region)
        await self.check_post_confirm_address_input_yes_code(display_region)
        await self.check_post_select_how_to_receive_input_no_selection(display_region)

    async def assert_post_request_access_code_select_how_to_receive_invalid(self, display_region, region):
        await self.check_get_enter_address(display_region)
        await self.check_post_enter_address(display_region)
        await self.check_post_select_address(display_region, region)
        await self.check_post_confirm_address_input_yes_code(display_region)
        await self.check_post_select_how_to_receive_input_invalid(display_region)

    async def assert_post_request_access_code_enter_mobile_invalid(self, display_region, region):
        await self.check_get_enter_address(display_region)
        await self.check_post_enter_address(display_region)
        await self.check_post_select_address(display_region, region)
        await self.check_post_confirm_address_input_yes_code(display_region)
        await self.check_post_select_how_to_receive_input_sms(display_region)
        await self.check_post_enter_mobile_input_invalid(display_region)

    async def assert_post_request_access_code_enter_mobile_empty(self, display_region, region):
        await self.check_get_enter_address(display_region)
        await self.check_post_enter_address(display_region)
        await self.check_post_select_address(display_region, region)
        await self.check_post_confirm_address_input_yes_code(display_region)
        await self.check_post_select_how_to_receive_input_sms(display_region)
        await self.check_post_enter_mobile_input_empty(display_region)

    async def assert_request_access_code_confirm_send_by_text_no(self, display_region, region):
        await self.check_get_enter_address(display_region)
        await self.check_post_enter_address(display_region)
        await self.check_post_select_address(display_region, region)
        await self.check_post_confirm_address_input_yes_code(display_region)
        await self.check_post_select_how_to_receive_input_sms(display_region)
        await self.check_post_enter_mobile(display_region)
        await self.check_post_confirm_send_by_text_input_no(display_region)

    async def assert_request_access_code_confirm_send_by_text_no_selection(self, display_region, region):
        await self.check_get_enter_address(display_region)
        await self.check_post_enter_address(display_region)
        await self.check_post_select_address(display_region, region)
        await self.check_post_confirm_address_input_yes_code(display_region)
        await self.check_post_select_how_to_receive_input_sms(display_region)
        await self.check_post_enter_mobile(display_region)
        await self.check_post_confirm_send_by_text_input_no_selection(display_region)

    async def assert_request_access_code_confirm_send_by_text_invalid(self, display_region, region):
        await self.check_get_enter_address(display_region)
        await self.check_post_enter_address(display_region)
        await self.check_post_select_address(display_region, region)
        await self.check_post_confirm_address_input_yes_code(display_region)
        await self.check_post_select_how_to_receive_input_sms(display_region)
        await self.check_post_enter_mobile(display_region)
        await self.check_post_confirm_send_by_text_input_invalid(display_region)

    async def assert_request_access_code_confirm_send_by_text_get_fulfilment_error(self, display_region, region):
        await self.check_get_enter_address(display_region)
        await self.check_post_enter_address(display_region)
        await self.check_post_select_address(display_region, region)
        await self.check_post_confirm_address_input_yes_code(display_region)
        await self.check_post_select_how_to_receive_input_sms(display_region)
        await self.check_post_enter_mobile(display_region)
        await self.check_post_confirm_send_by_text_error_from_get_fulfilment(display_region, region)

    async def assert_request_access_code_confirm_send_by_text_request_fulfilment_error(self, display_region, region):
        await self.check_get_enter_address(display_region)
        await self.check_post_enter_address(display_region)
        await self.check_post_select_address(display_region, region)
        await self.check_post_confirm_address_input_yes_code(display_region)
        await self.check_post_select_how_to_receive_input_sms(display_region)
        await self.check_post_enter_mobile(display_region)
        await self.check_post_confirm_send_by_text_error_from_request_fulfilment(display_region)

    async def assert_request_access_code_confirm_send_by_text_request_fulfilment_error_429(
            self, display_region, region):
        await self.check_get_enter_address(display_region)
        await self.check_post_enter_address(display_region)
        await self.check_post_select_address(display_region, region)
        await self.check_post_confirm_address_input_yes_code(display_region)
        await self.check_post_select_how_to_receive_input_sms(display_region)
        await self.check_post_enter_mobile(display_region)
        await self.check_post_confirm_send_by_text_error_429_from_request_fulfilment(display_region)

    async def assert_request_access_code_post_enter_name_error(self, display_region, region, error):
        if error == 'only_spaces':
            data = self.request_common_enter_name_form_data_only_spaces
        elif error == 'no_first':
            data = self.request_common_enter_name_form_data_no_first
        elif error == 'no_last':
            data = self.request_common_enter_name_form_data_no_last
        elif error == 'overlength_first':
            data = self.request_common_enter_name_form_data_overlength_firstname
        elif error == 'overlength_last':
            data = self.request_common_enter_name_form_data_overlength_lastname
        else:
            data = self.common_form_data_empty
        await self.check_get_enter_address(display_region)
        await self.check_post_enter_address(display_region)
        await self.check_post_select_address(display_region, region)
        await self.check_post_confirm_address_input_yes_code(display_region)
        await self.check_post_select_how_to_receive_input_post(display_region)
        await self.check_post_enter_name_inputs_error(display_region, data)

    async def assert_request_access_code_post_confirm_send_by_post_input_error(self, display_region, region, error):
        if error == 'invalid':
            data = self.request_common_confirm_send_by_post_data_invalid
        else:
            data = self.common_form_data_empty
        await self.check_get_enter_address(display_region)
        await self.check_post_enter_address(display_region)
        await self.check_post_select_address(display_region, region)
        await self.check_post_confirm_address_input_yes_code(display_region)
        await self.check_post_select_how_to_receive_input_post(display_region)
        await self.check_post_enter_name(display_region)
        await self.check_post_confirm_send_by_post_input_invalid_or_no_selection(display_region, data)

    async def assert_request_access_code_post_confirm_send_by_post_option_no(self, display_region, region):
        await self.check_get_enter_address(display_region)
        await self.check_post_enter_address(display_region)
        await self.check_post_select_address(display_region, region)
        await self.check_post_confirm_address_input_yes_code(display_region)
        await self.check_post_select_how_to_receive_input_post(display_region)
        await self.check_post_enter_name(display_region)
        await self.check_post_confirm_send_by_post_input_no(display_region)

    async def assert_request_access_code_post_code_sent_post(self, display_region, region):
        await self.check_get_enter_address(display_region)
        await self.check_post_enter_address(display_region)
        await self.check_post_select_address(display_region, region)
        await self.check_post_confirm_address_input_yes_code(display_region)
        await self.check_post_select_how_to_receive_input_post(display_region)
        await self.check_post_enter_name(display_region)
        await self.check_post_confirm_send_by_post_input_yes(display_region, region)

    async def assert_request_access_code_post_confirm_send_by_post_get_fulfilment_error(self, display_region, region):
        await self.check_get_enter_address(display_region)
        await self.check_post_enter_address(display_region)
        await self.check_post_select_address(display_region, region)
        await self.check_post_confirm_address_input_yes_code(display_region)
        await self.check_post_select_how_to_receive_input_post(display_region)
        await self.check_post_enter_name(display_region)
        await self.check_post_confirm_send_by_post_error_from_get_fulfilment(display_region, region)

    async def assert_request_access_code_post_confirm_send_by_post_request_fulfilment_error(
            self, display_region, region):
        await self.check_get_enter_address(display_region)
        await self.check_post_enter_address(display_region)
        await self.check_post_select_address(display_region, region)
        await self.check_post_confirm_address_input_yes_code(display_region)
        await self.check_post_select_how_to_receive_input_post(display_region)
        await self.check_post_enter_name(display_region)
        await self.check_post_confirm_send_by_post_error_from_request_fulfilment(display_region)

    async def assert_request_access_code_post_confirm_send_by_post_request_fulfilment_error_429(
            self, display_region, region):
        await self.check_get_enter_address(display_region)
        await self.check_post_enter_address(display_region)
        await self.check_post_select_address(display_region, region)
        await self.check_post_confirm_address_input_yes_code(display_region)
        await self.check_post_select_how_to_receive_input_post(display_region)
        await self.check_post_enter_name(display_region)
        await self.check_post_confirm_send_by_post_error_429_from_request_fulfilment_uac(display_region)

    @unittest_run_loop
    async def test_request_access_code_sms_happy_path_ew_e(self):
        await self.assert_request_access_code_sms_happy_path('en', 'E')

    @unittest_run_loop
    async def test_request_access_code_sms_happy_path_ew_w(self):
        await self.assert_request_access_code_sms_happy_path('en', 'W')

    @unittest_run_loop
    async def test_request_access_code_sms_happy_path_cy(self):
        await self.assert_request_access_code_sms_happy_path('cy', 'W')

    @unittest_run_loop
    async def test_post_request_access_code_enter_address_no_results_ew(self):
        await self.assert_post_request_access_code_enter_address_no_results('en')

    @unittest_run_loop
    async def test_post_request_access_code_enter_address_no_results_cy(self):
        await self.assert_post_request_access_code_enter_address_no_results('cy')

    @unittest_run_loop
    async def test_post_request_access_code_get_ai_postcode_error_en(self):
        await self.assert_post_request_access_code_get_ai_postcode_error('en')

    @unittest_run_loop
    async def test_post_request_access_code_get_ai_postcode_error_cy(self):
        await self.assert_post_request_access_code_get_ai_postcode_error('cy')

    @unittest_run_loop
    async def test_get_request_access_code_address_not_found_ew(self):
        await self.assert_get_request_access_code_address_not_found('en')

    @unittest_run_loop
    async def test_get_request_access_code_address_not_found_cy(self):
        await self.assert_get_request_access_code_address_not_found('cy')

    @unittest_run_loop
    async def test_post_request_access_code_enter_address_empty_ew(self):
        await self.assert_post_request_access_code_enter_address_empty('en')

    @unittest_run_loop
    async def test_post_request_access_code_enter_address_empty_cy(self):
        await self.assert_post_request_access_code_enter_address_empty('cy')

    @unittest_run_loop
    async def test_post_request_access_code_enter_address_invalid_postcode_ew(self):
        await self.assert_post_request_access_code_enter_address_invalid_postcode('en')

    @unittest_run_loop
    async def test_post_request_access_code_enter_address_invalid_postcode_cy(self):
        await self.assert_post_request_access_code_enter_address_invalid_postcode('cy')

    @unittest_run_loop
    async def test_get_request_access_code_confirm_address_get_cases_error_ew(self):
        await self.assert_get_request_access_code_confirm_address_get_cases_error('en')

    @unittest_run_loop
    async def test_get_request_access_code_confirm_address_get_cases_error_cy(self):
        await self.assert_get_request_access_code_confirm_address_get_cases_error('cy')

    @unittest_run_loop
    async def test_get_request_access_code_enter_address_finder_ew_e(self):
        await self.assert_get_request_access_code_enter_address_finder('en', 'E')

    @unittest_run_loop
    async def test_get_request_access_code_enter_address_finder_ew_w(self):
        await self.assert_get_request_access_code_enter_address_finder('en', 'W')

    @unittest_run_loop
    async def test_get_request_access_code_enter_address_finder_cy(self):
        await self.assert_get_request_access_code_enter_address_finder('cy', 'W')

    @unittest_run_loop
    async def test_get_request_individual_confirm_address_data_no_ew_e(self):
        await self.assert_get_request_access_code_confirm_address_data_no('en', 'E')

    @unittest_run_loop
    async def test_get_request_individual_confirm_address_data_no_ew_w(self):
        await self.assert_get_request_access_code_confirm_address_data_no('en', 'W')

    @unittest_run_loop
    async def test_get_request_individual_confirm_address_data_no_cy(self):
        await self.assert_get_request_access_code_confirm_address_data_no('cy', 'W')

    @unittest_run_loop
    async def test_get_request_access_code_confirm_address_data_invalid_ew_e(self):
        await self.assert_get_request_access_code_confirm_address_data_invalid('en', 'E')

    @unittest_run_loop
    async def test_get_request_access_code_confirm_address_data_invalid_ew_w(self):
        await self.assert_get_request_access_code_confirm_address_data_invalid('en', 'W')

    @unittest_run_loop
    async def test_get_request_access_code_confirm_address_data_invalid_cy(self):
        await self.assert_get_request_access_code_confirm_address_data_invalid('cy', 'W')

    @unittest_run_loop
    async def test_get_request_access_code_confirm_address_data_no_selection_ew_e(self):
        await self.assert_get_request_access_code_confirm_address_data_no_selection('en', 'E')

    @unittest_run_loop
    async def test_get_request_access_code_confirm_address_data_no_selection_ew_w(self):
        await self.assert_get_request_access_code_confirm_address_data_no_selection('en', 'W')

    @unittest_run_loop
    async def test_get_request_access_code_confirm_address_data_no_selection_cy(self):
        await self.assert_get_request_access_code_confirm_address_data_no_selection('cy', 'W')

    @unittest_run_loop
    async def test_post_request_access_code_select_address_no_selection_ew(self):
        await self.assert_post_request_access_code_select_address_no_selection('en')

    @unittest_run_loop
    async def test_post_request_access_code_select_address_no_selection_cy(self):
        await self.assert_post_request_access_code_select_address_no_selection('cy')

    @unittest_run_loop
    async def test_post_request_access_code_select_address_no_case_ew(self):
        await self.assert_post_request_access_code_select_address_no_case('en')

    @unittest_run_loop
    async def test_post_request_access_code_select_address_no_case_cy(self):
        await self.assert_post_request_access_code_select_address_no_case('cy')

    @unittest_run_loop
    async def test_post_request_access_code_select_how_to_receive_no_selection_ew_e(self):
        await self.assert_post_request_access_code_select_how_to_receive_no_selection('en', 'E')

    @unittest_run_loop
    async def test_post_request_access_code_select_how_to_receive_no_selection_ew_w(self):
        await self.assert_post_request_access_code_select_how_to_receive_no_selection('en', 'W')

    @unittest_run_loop
    async def test_post_request_access_code_select_how_to_receive_no_selection_cy(self):
        await self.assert_post_request_access_code_select_how_to_receive_no_selection('cy', 'W')

    @unittest_run_loop
    async def test_post_request_access_code_select_how_to_receive_input_invalid_ew_e(self):
        await self.assert_post_request_access_code_select_how_to_receive_invalid('en', 'E')

    @unittest_run_loop
    async def test_post_request_access_code_select_how_to_receive_input_invalid_ew_w(self):
        await self.assert_post_request_access_code_select_how_to_receive_invalid('en', 'W')

    @unittest_run_loop
    async def test_post_request_access_code_select_how_to_receive_input_invalid_cy(self):
        await self.assert_post_request_access_code_select_how_to_receive_invalid('cy', 'W')

    @unittest_run_loop
    async def test_post_request_access_code_enter_mobile_invalid_ew_e(self):
        await self.assert_post_request_access_code_enter_mobile_invalid('en', 'E')

    @unittest_run_loop
    async def test_post_request_access_code_enter_mobile_invalid_ew_w(self):
        await self.assert_post_request_access_code_enter_mobile_invalid('en', 'W')

    @unittest_run_loop
    async def test_post_request_access_code_enter_mobile_invalid_cy(self):
        await self.assert_post_request_access_code_enter_mobile_invalid('cy', 'W')

    @unittest_run_loop
    async def test_post_request_access_code_enter_mobile_empty_ew_e(self):
        await self.assert_post_request_access_code_enter_mobile_empty('en', 'E')

    @unittest_run_loop
    async def test_post_request_access_code_enter_mobile_empty_ew_w(self):
        await self.assert_post_request_access_code_enter_mobile_empty('en', 'W')

    @unittest_run_loop
    async def test_post_request_access_code_enter_mobile_empty_cy(self):
        await self.assert_post_request_access_code_enter_mobile_empty('cy', 'W')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_no_ew_e(self):
        await self.assert_request_access_code_confirm_send_by_text_no('en', 'E')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_no_ew_w(self):
        await self.assert_request_access_code_confirm_send_by_text_no('en', 'W')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_no_cy(self):
        await self.assert_request_access_code_confirm_send_by_text_no('cy', 'W')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_empty_ew_e(self):
        await self.assert_request_access_code_confirm_send_by_text_no_selection('en', 'E')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_empty_ew_w(self):
        await self.assert_request_access_code_confirm_send_by_text_no_selection('en', 'W')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_empty_cy(self):
        await self.assert_request_access_code_confirm_send_by_text_no_selection('cy', 'W')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_invalid_ew_e(self):
        await self.assert_request_access_code_confirm_send_by_text_invalid('en', 'E')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_invalid_ew_w(self):
        await self.assert_request_access_code_confirm_send_by_text_invalid('en', 'W')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_invalid_cy(self):
        await self.assert_request_access_code_confirm_send_by_text_invalid('cy', 'W')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_get_fulfilment_error_ew_e(self):
        await self.assert_request_access_code_confirm_send_by_text_get_fulfilment_error('en', 'E')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_get_fulfilment_error_ew_w(self):
        await self.assert_request_access_code_confirm_send_by_text_get_fulfilment_error('en', 'W')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_get_fulfilment_error_cy(self):
        await self.assert_request_access_code_confirm_send_by_text_get_fulfilment_error('cy', 'W')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_request_fulfilment_error_ew_e(self):
        await self.assert_request_access_code_confirm_send_by_text_request_fulfilment_error('en', 'E')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_request_fulfilment_error_ew_w(self):
        await self.assert_request_access_code_confirm_send_by_text_request_fulfilment_error('en', 'W')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_request_fulfilment_error_cy(self):
        await self.assert_request_access_code_confirm_send_by_text_request_fulfilment_error('cy', 'W')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_request_fulfilment_error_429_ew_e(self):
        await self.assert_request_access_code_confirm_send_by_text_request_fulfilment_error_429('en', 'E')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_request_fulfilment_error_429_ew_w(self):
        await self.assert_request_access_code_confirm_send_by_text_request_fulfilment_error_429('en', 'W')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_request_fulfilment_error_429_cy(self):
        await self.assert_request_access_code_confirm_send_by_text_request_fulfilment_error_429('cy', 'W')

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_empty_ew_e(self):
        await self.assert_request_access_code_post_enter_name_error('en', 'E', 'empty')

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_empty_ew_w(self):
        await self.assert_request_access_code_post_enter_name_error('en', 'W', 'empty')

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_empty_cy(self):
        await self.assert_request_access_code_post_enter_name_error('cy', 'W', 'empty')

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_only_spaces_ew_e(self):
        await self.assert_request_access_code_post_enter_name_error('en', 'E', 'only_spaces')

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_only_spaces_ew_w(self):
        await self.assert_request_access_code_post_enter_name_error('en', 'W', 'only_spaces')

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_only_spaces_cy(self):
        await self.assert_request_access_code_post_enter_name_error('cy', 'W', 'only_spaces')

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_no_first_ew_e(self):
        await self.assert_request_access_code_post_enter_name_error('en', 'E', 'no_first')

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_no_first_ew_w(self):
        await self.assert_request_access_code_post_enter_name_error('en', 'W', 'no_first')

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_no_first_cy(self):
        await self.assert_request_access_code_post_enter_name_error('cy', 'W', 'no_first')

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_no_last_ew_e(self):
        await self.assert_request_access_code_post_enter_name_error('en', 'E', 'no_last')

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_no_last_ew_w(self):
        await self.assert_request_access_code_post_enter_name_error('en', 'W', 'no_last')

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_no_last_cy(self):
        await self.assert_request_access_code_post_enter_name_error('cy', 'W', 'no_last')

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_overlength_first_ew_e(self):
        await self.assert_request_access_code_post_enter_name_error('en', 'E', 'overlength_first')

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_overlength_first_ew_w(self):
        await self.assert_request_access_code_post_enter_name_error('en', 'W', 'overlength_first')

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_overlength_first_cy(self):
        await self.assert_request_access_code_post_enter_name_error('cy', 'W', 'overlength_first')

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_overlength_last_ew_e(self):
        await self.assert_request_access_code_post_enter_name_error('en', 'E', 'overlength_last')

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_overlength_last_ew_w(self):
        await self.assert_request_access_code_post_enter_name_error('en', 'W', 'overlength_last')

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_overlength_last_cy(self):
        await self.assert_request_access_code_post_enter_name_error('cy', 'W', 'overlength_last')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_empty_ew_e(self):
        await self.assert_request_access_code_post_confirm_send_by_post_input_error('en', 'E', 'empty')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_empty_ew_w(self):
        await self.assert_request_access_code_post_confirm_send_by_post_input_error('en', 'W', 'empty')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_empty_cy(self):
        await self.assert_request_access_code_post_confirm_send_by_post_input_error('cy', 'W', 'empty')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_input_invalid_ew_e(self):
        await self.assert_request_access_code_post_confirm_send_by_post_input_error('en', 'E', 'invalid')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_input_invalid_ew_w(self):
        await self.assert_request_access_code_post_confirm_send_by_post_input_error('en', 'W', 'invalid')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_input_invalid_cy(self):
        await self.assert_request_access_code_post_confirm_send_by_post_input_error('cy', 'W', 'invalid')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_option_no_ew_e(self):
        await self.assert_request_access_code_post_confirm_send_by_post_option_no('en', 'E')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_option_no_ew_w(self):
        await self.assert_request_access_code_post_confirm_send_by_post_option_no('en', 'W')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_option_no_cy(self):
        await self.assert_request_access_code_post_confirm_send_by_post_option_no('cy', 'W')

    @unittest_run_loop
    async def test_request_access_code_post_code_sent_post_ew_e(self):
        await self.assert_request_access_code_post_code_sent_post('en', 'E')

    @unittest_run_loop
    async def test_request_access_code_post_code_sent_post_ew_w(self):
        await self.assert_request_access_code_post_code_sent_post('en', 'W')

    @unittest_run_loop
    async def test_request_access_code_post_code_sent_post_cy(self):
        await self.assert_request_access_code_post_code_sent_post('cy', 'W')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_get_fulfilment_error_ew_e(self):
        await self.assert_request_access_code_post_confirm_send_by_post_get_fulfilment_error('en', 'E')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_get_fulfilment_error_ew_w(self):
        await self.assert_request_access_code_post_confirm_send_by_post_get_fulfilment_error('en', 'W')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_get_fulfilment_error_cy(self):
        await self.assert_request_access_code_post_confirm_send_by_post_get_fulfilment_error('cy', 'W')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_request_fulfilment_error_ew_e(self):
        await self.assert_request_access_code_post_confirm_send_by_post_request_fulfilment_error('en', 'E')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_request_fulfilment_error_ew_w(self):
        await self.assert_request_access_code_post_confirm_send_by_post_request_fulfilment_error('en', 'W')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_request_fulfilment_error_cy(self):
        await self.assert_request_access_code_post_confirm_send_by_post_request_fulfilment_error('cy', 'W')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_request_fulfilment_error_429_ew_e(self):
        await self.assert_request_access_code_post_confirm_send_by_post_request_fulfilment_error_429('en', 'E')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_request_fulfilment_error_429_ew_w(self):
        await self.assert_request_access_code_post_confirm_send_by_post_request_fulfilment_error_429('en', 'W')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_request_fulfilment_error_429_cy(self):
        await self.assert_request_access_code_post_confirm_send_by_post_request_fulfilment_error_429('cy', 'W')
