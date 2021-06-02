from aiohttp.test_utils import unittest_run_loop
from .helpers import TestHelpers


# noinspection PyTypeChecker
class TestRequestHandlersAccessCode(TestHelpers):

    user_journey = 'request'
    sub_user_journey = 'access-code'

    @unittest_run_loop
    async def test_request_access_code_sms_happy_path_hh_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'HH', 'E')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en', 'household')
        await self.check_post_confirm_send_by_text(
            self.post_request_access_code_confirm_send_by_text_en, 'en', 'E', 'false')

    @unittest_run_loop
    async def test_request_access_code_sms_happy_path_hh_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'HH', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en', 'household')
        await self.check_post_confirm_send_by_text(
            self.post_request_access_code_confirm_send_by_text_en, 'en', 'W', 'false')

    @unittest_run_loop
    async def test_request_access_code_sms_happy_path_hh_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'HH', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_cy, 'cy', 'household')
        await self.check_post_confirm_send_by_text(
            self.post_request_access_code_confirm_send_by_text_cy, 'cy', 'W', 'false')

    @unittest_run_loop
    async def test_post_request_access_code_enter_address_no_results_ew(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address_input_returns_no_results(
            self.post_request_access_code_enter_address_en, 'en')

    @unittest_run_loop
    async def test_post_request_access_code_enter_address_no_results_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address_input_returns_no_results(
            self.post_request_access_code_enter_address_cy, 'cy')

    @unittest_run_loop
    async def test_post_request_access_code_get_ai_postcode_error(self):
        await self.check_post_enter_address_error_from_ai(self.get_request_access_code_enter_address_en,
                                                          self.post_request_access_code_enter_address_en, 'en', 500)
        await self.check_post_enter_address_error_from_ai(self.get_request_access_code_enter_address_cy,
                                                          self.post_request_access_code_enter_address_cy, 'cy', 500)
        await self.check_post_enter_address_error_503_from_ai(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address_error_503_from_ai(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address_error_from_ai(self.get_request_access_code_enter_address_en,
                                                          self.post_request_access_code_enter_address_en, 'en', 403)
        await self.check_post_enter_address_error_from_ai(self.get_request_access_code_enter_address_cy,
                                                          self.post_request_access_code_enter_address_cy, 'cy', 403)
        await self.check_post_enter_address_error_from_ai(self.get_request_access_code_enter_address_en,
                                                          self.post_request_access_code_enter_address_en, 'en', 401)
        await self.check_post_enter_address_error_from_ai(self.get_request_access_code_enter_address_cy,
                                                          self.post_request_access_code_enter_address_cy, 'cy', 401)
        await self.check_post_enter_address_error_from_ai(self.get_request_access_code_enter_address_en,
                                                          self.post_request_access_code_enter_address_en, 'en', 400)
        await self.check_post_enter_address_error_from_ai(self.get_request_access_code_enter_address_cy,
                                                          self.post_request_access_code_enter_address_cy, 'cy', 400)
        await self.check_post_enter_address_error_from_ai(self.get_request_access_code_enter_address_en,
                                                          self.post_request_access_code_enter_address_en, 'en', 429)
        await self.check_post_enter_address_error_from_ai(self.get_request_access_code_enter_address_cy,
                                                          self.post_request_access_code_enter_address_cy, 'cy', 429)
        await self.check_post_enter_address_connection_error_from_ai(
            self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address_connection_error_from_ai(
            self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address_connection_error_from_ai(
            self.post_request_access_code_enter_address_en, 'en', epoch='test')
        await self.check_post_enter_address_connection_error_from_ai(
            self.post_request_access_code_enter_address_cy, 'cy', epoch='test')

    @unittest_run_loop
    async def test_get_request_access_code_address_not_found_ew(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address_address_not_found(
            self.post_request_access_code_select_address_en, 'en')

    @unittest_run_loop
    async def test_get_request_access_code_address_not_found_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address_address_not_found(
            self.post_request_access_code_select_address_cy, 'cy')

    @unittest_run_loop
    async def test_post_request_access_code_enter_address_invalid_postcode_ew(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address_input_invalid(self.post_request_access_code_enter_address_en, 'en')

    @unittest_run_loop
    async def test_post_request_access_code_enter_address_invalid_postcode_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address_input_invalid(self.post_request_access_code_enter_address_cy, 'cy')

    @unittest_run_loop
    async def test_get_request_access_code_confirm_address_get_cases_error_ew(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address_error_from_get_cases(self.post_request_access_code_select_address_en, 'en')

    @unittest_run_loop
    async def test_get_request_access_code_confirm_address_get_cases_error_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address_error_from_get_cases(self.post_request_access_code_select_address_cy, 'cy')

    @unittest_run_loop
    async def test_get_request_access_code_confirm_address_data_no_ew(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'HH', 'E')
        await self.check_post_confirm_address_input_no(self.post_request_access_code_confirm_address_en, 'en')

    @unittest_run_loop
    async def test_get_request_individual_confirm_address_data_no_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'HH', 'W')
        await self.check_post_confirm_address_input_no(self.post_request_access_code_confirm_address_cy, 'cy')

    @unittest_run_loop
    async def test_get_request_access_code_confirm_address_data_invalid_ew(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'HH', 'E')
        await self.check_post_confirm_address_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_address_en, 'en', self.common_confirm_address_input_invalid)

    @unittest_run_loop
    async def test_get_request_access_code_confirm_address_data_invalid_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'HH', 'W')
        await self.check_post_confirm_address_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_address_cy, 'cy', self.common_confirm_address_input_invalid)

    @unittest_run_loop
    async def test_get_request_access_code_confirm_address_no_selection_ew(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'HH', 'E')
        await self.check_post_confirm_address_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_address_en, 'en', self.common_form_data_empty)

    @unittest_run_loop
    async def test_get_request_access_code_confirm_address_no_selection_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'HH', 'W')
        await self.check_post_confirm_address_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_address_cy, 'cy', self.common_form_data_empty)

    @unittest_run_loop
    async def test_post_request_access_code_select_address_no_selection_ew(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address_no_selection_made(
            self.post_request_access_code_select_address_en, 'en')

    @unittest_run_loop
    async def test_post_request_access_code_select_address_no_selection_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address_no_selection_made(
            self.post_request_access_code_select_address_cy, 'cy')

    @unittest_run_loop
    async def test_post_request_access_code_select_how_to_receive_no_selection_hh_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'HH', 'E')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_select_how_to_receive_input_invalid_or_no_selection(
            self.post_request_access_code_select_how_to_receive_en, 'en', self.common_form_data_empty)

    @unittest_run_loop
    async def test_post_request_access_code_select_how_to_receive_no_selection_hh_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'HH', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_select_how_to_receive_input_invalid_or_no_selection(
            self.post_request_access_code_select_how_to_receive_en, 'en', self.common_form_data_empty)

    @unittest_run_loop
    async def test_post_request_access_code_select_how_to_receive_no_selection_hh_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'HH', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_post_select_how_to_receive_input_invalid_or_no_selection(
            self.post_request_access_code_select_how_to_receive_cy, 'cy', self.common_form_data_empty)

    @unittest_run_loop
    async def test_post_request_access_code_select_how_to_receive_input_invalid_hh_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'HH', 'E')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_select_how_to_receive_input_invalid_or_no_selection(
            self.post_request_access_code_select_how_to_receive_en, 'en',
            self.request_code_select_how_to_receive_data_invalid)

    @unittest_run_loop
    async def test_post_request_access_code_select_how_to_receive_input_invalid_hh_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'HH', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_select_how_to_receive_input_invalid_or_no_selection(
            self.post_request_access_code_select_how_to_receive_en, 'en',
            self.request_code_select_how_to_receive_data_invalid)

    @unittest_run_loop
    async def test_post_request_access_code_select_how_to_receive_input_invalid_hh_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'HH', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_post_select_how_to_receive_input_invalid_or_no_selection(
            self.post_request_access_code_select_how_to_receive_cy, 'cy',
            self.request_code_select_how_to_receive_data_invalid)

    @unittest_run_loop
    async def test_post_request_access_code_enter_mobile_invalid_hh_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'HH', 'E')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_mobile_input_invalid(self.post_request_access_code_enter_mobile_en, 'en')

    @unittest_run_loop
    async def test_post_request_access_code_enter_mobile_invalid_hh_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'HH', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_mobile_input_invalid(self.post_request_access_code_enter_mobile_en, 'en')

    @unittest_run_loop
    async def test_post_request_access_code_enter_mobile_invalid_hh_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'HH', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_mobile_input_invalid(self.post_request_access_code_enter_mobile_cy, 'cy')

    @unittest_run_loop
    async def test_post_request_access_code_enter_mobile_empty_hh_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'HH', 'E')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_mobile_input_empty(self.post_request_access_code_enter_mobile_en, 'en')

    @unittest_run_loop
    async def test_post_request_access_code_enter_mobile_empty_hh_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'HH', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_mobile_input_empty(self.post_request_access_code_enter_mobile_en, 'en')

    @unittest_run_loop
    async def test_post_request_access_code_enter_mobile_empty_hh_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'HH', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_mobile_input_empty(self.post_request_access_code_enter_mobile_cy, 'cy')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_no_hh_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'HH', 'E')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en', 'household')
        await self.check_post_confirm_send_by_text_input_no(self.post_request_access_code_confirm_send_by_text_en, 'en')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_no_hh_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'HH', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en', 'household')
        await self.check_post_confirm_send_by_text_input_no(self.post_request_access_code_confirm_send_by_text_en, 'en')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_no_hh_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'HH', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_cy, 'cy', 'household')
        await self.check_post_confirm_send_by_text_input_no(self.post_request_access_code_confirm_send_by_text_cy, 'cy')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_empty_hh_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'HH', 'E')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en', 'household')
        await self.check_post_confirm_send_by_text_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_send_by_text_en, 'en',
            self.request_code_mobile_confirmation_data_empty, 'household')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_empty_hh_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'HH', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en', 'household')
        await self.check_post_confirm_send_by_text_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_send_by_text_en, 'en',
            self.request_code_mobile_confirmation_data_empty, 'household')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_empty_hh_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'HH', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_cy, 'cy', 'household')
        await self.check_post_confirm_send_by_text_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_send_by_text_cy, 'cy',
            self.request_code_mobile_confirmation_data_empty, 'household')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_invalid_hh_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'HH', 'E')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en', 'household')
        await self.check_post_confirm_send_by_text_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_send_by_text_en, 'en',
            self.request_code_mobile_confirmation_data_invalid, 'household')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_invalid_hh_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'HH', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en', 'household')
        await self.check_post_confirm_send_by_text_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_send_by_text_en, 'en',
            self.request_code_mobile_confirmation_data_invalid, 'household')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_invalid_hh_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'HH', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_cy, 'cy', 'household')
        await self.check_post_confirm_send_by_text_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_send_by_text_cy, 'cy',
            self.request_code_mobile_confirmation_data_invalid, 'household')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_get_fulfilment_error_hh_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'HH', 'E')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en', 'household')
        await self.check_post_confirm_send_by_text_error_from_get_fulfilment(
            self.post_request_access_code_confirm_send_by_text_en, 'en', 'HH', 'E', 'false')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_get_fulfilment_error_hh_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'HH', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en', 'household')
        await self.check_post_confirm_send_by_text_error_from_get_fulfilment(
            self.post_request_access_code_confirm_send_by_text_en, 'en', 'HH', 'W', 'false')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_get_fulfilment_error_hh_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'HH', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_cy, 'cy', 'household')
        await self.check_post_confirm_send_by_text_error_from_get_fulfilment(
            self.post_request_access_code_confirm_send_by_text_cy, 'cy', 'HH', 'W', 'false')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_request_fulfilment_error_hh_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'HH', 'E')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en', 'household')
        await self.check_post_confirm_send_by_text_error_from_request_fulfilment(
            self.post_request_access_code_confirm_send_by_text_en, 'en')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_request_fulfilment_error_hh_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'HH', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en', 'household')
        await self.check_post_confirm_send_by_text_error_from_request_fulfilment(
            self.post_request_access_code_confirm_send_by_text_en, 'en')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_request_fulfilment_error_hh_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'HH', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_cy, 'cy', 'household')
        await self.check_post_confirm_send_by_text_error_from_request_fulfilment(
            self.post_request_access_code_confirm_send_by_text_cy, 'cy')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_request_fulfilment_error_429_hh_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'HH', 'E')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en', 'household')
        await self.check_post_confirm_send_by_text_error_429_from_request_fulfilment(
            self.post_request_access_code_confirm_send_by_text_en, 'en')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_texte_request_fulfilment_error_429_hh_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'HH', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_en, 'en', 'household')
        await self.check_post_confirm_send_by_text_error_429_from_request_fulfilment(
            self.post_request_access_code_confirm_send_by_text_en, 'en')

    @unittest_run_loop
    async def test_request_access_code_confirm_send_by_text_request_fulfilment_error_429_hh_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'HH', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_post_select_how_to_receive_input_sms(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_mobile(self.post_request_access_code_enter_mobile_cy, 'cy', 'household')
        await self.check_post_confirm_send_by_text_error_429_from_request_fulfilment(
            self.post_request_access_code_confirm_send_by_text_cy, 'cy')

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_empty_hh_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'HH', 'E')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_en, 'en',
                                                      self.common_form_data_empty)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_empty_hh_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'HH', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_en, 'en',
                                                      self.common_form_data_empty)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_empty_hh_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'HH', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_cy, 'cy',
                                                      self.common_form_data_empty)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_empty_hh_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'HH', 'E')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_en, 'en',
                                                      self.request_common_enter_name_form_data_only_spaces)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_only_spaces_hh_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'HH', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_en, 'en',
                                                      self.request_common_enter_name_form_data_only_spaces)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_only_spaces_hh_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'HH', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_cy, 'cy',
                                                      self.request_common_enter_name_form_data_only_spaces)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_no_first_hh_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'HH', 'E')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_en, 'en',
                                                      self.request_common_enter_name_form_data_no_first)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_no_first_hh_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'HH', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_en, 'en',
                                                      self.request_common_enter_name_form_data_no_first)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_no_first_hh_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'HH', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_cy, 'cy',
                                                      self.request_common_enter_name_form_data_no_first)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_no_last_hh_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'HH', 'E')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_en, 'en',
                                                      self.request_common_enter_name_form_data_no_last)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_no_last_hh_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'HH', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_en, 'en',
                                                      self.request_common_enter_name_form_data_no_last)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_no_last_hh_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'HH', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_cy, 'cy',
                                                      self.request_common_enter_name_form_data_no_last)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_overlength_first_hh_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'HH', 'E')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_en, 'en',
                                                      self.request_common_enter_name_form_data_overlong_firstname)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_overlength_first_hh_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'HH', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_en, 'en',
                                                      self.request_common_enter_name_form_data_overlong_firstname)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_overlength_first_hh_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'HH', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_cy, 'cy',
                                                      self.request_common_enter_name_form_data_overlong_firstname)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_overlength_last_hh_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'HH', 'E')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_en, 'en',
                                                      self.request_common_enter_name_form_data_overlong_lastname)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_overlength_last_hh_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'HH', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_en, 'en',
                                                      self.request_common_enter_name_form_data_overlong_lastname)

    @unittest_run_loop
    async def test_request_access_code_post_enter_name_overlength_last_hh_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'HH', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_name_inputs_error(self.post_request_access_code_enter_name_cy, 'cy',
                                                      self.request_common_enter_name_form_data_overlong_lastname)

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_empty_hh_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'HH', 'E')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'household')
        await self.check_post_confirm_send_by_post_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_send_by_post_en, 'en', self.common_form_data_empty, 'household')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_empty_hh_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'HH', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'household')
        await self.check_post_confirm_send_by_post_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_send_by_post_en, 'en', self.common_form_data_empty, 'household')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_empty_hh_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'HH', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_cy, 'cy', 'household')
        await self.check_post_confirm_send_by_post_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_send_by_post_cy, 'cy', self.common_form_data_empty, 'household')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_input_invalid_hh_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'HH', 'E')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'household')
        await self.check_post_confirm_send_by_post_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_send_by_post_en, 'en',
            self.request_common_confirm_send_by_post_data_invalid, 'household')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_input_invalid_hh_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'HH', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'household')
        await self.check_post_confirm_send_by_post_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_send_by_post_en, 'en',
            self.request_common_confirm_send_by_post_data_invalid, 'household')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_input_invalid_hh_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'HH', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_cy, 'cy', 'household')
        await self.check_post_confirm_send_by_post_input_invalid_or_no_selection(
            self.post_request_access_code_confirm_send_by_post_cy, 'cy',
            self.request_common_confirm_send_by_post_data_invalid, 'household')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_option_no_hh_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'HH', 'E')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'household')
        await self.check_post_confirm_send_by_post_input_no(
            self.post_request_access_code_confirm_send_by_post_en, 'en')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_option_no_hh_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'HH', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'household')
        await self.check_post_confirm_send_by_post_input_no(
            self.post_request_access_code_confirm_send_by_post_en, 'en')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_option_no_hh_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'HH', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_cy, 'cy', 'household')
        await self.check_post_confirm_send_by_post_input_no(
            self.post_request_access_code_confirm_send_by_post_cy, 'cy')

    @unittest_run_loop
    async def test_request_access_code_post_code_sent_post_hh_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'HH', 'E')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'household')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_access_code_confirm_send_by_post_en, 'en', 'E', 'false')

    @unittest_run_loop
    async def test_request_access_code_post_code_sent_post_hh_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'HH', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'household')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_access_code_confirm_send_by_post_en, 'en', 'W', 'false')

    @unittest_run_loop
    async def test_request_access_code_post_code_sent_post_hh_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'HH', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_cy, 'cy', 'household')
        await self.check_post_confirm_send_by_post_input_yes(
            self.post_request_access_code_confirm_send_by_post_cy, 'cy', 'W', 'false')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_get_fulfilment_error_hh_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'HH', 'E')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'household')
        await self.check_post_confirm_send_by_post_error_from_get_fulfilment(
            self.post_request_access_code_confirm_send_by_post_en, 'en', 'E', 'UAC', 'false')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_get_fulfilment_error_hh_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'HH', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'household')
        await self.check_post_confirm_send_by_post_error_from_get_fulfilment(
            self.post_request_access_code_confirm_send_by_post_en, 'en', 'W', 'UAC', 'false')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_get_fulfilment_error_hh_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'HH', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_cy, 'cy', 'household')
        await self.check_post_confirm_send_by_post_error_from_get_fulfilment(
            self.post_request_access_code_confirm_send_by_post_cy, 'cy', 'W', 'UAC', 'false')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_request_fulfilment_error_hh_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'HH', 'E')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'household')
        await self.check_post_confirm_send_by_post_error_from_request_fulfilment(
            self.post_request_access_code_confirm_send_by_post_en, 'en')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_request_fulfilment_error_hh_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'HH', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'household')
        await self.check_post_confirm_send_by_post_error_from_request_fulfilment(
            self.post_request_access_code_confirm_send_by_post_en, 'en')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_request_fulfilment_error_hh_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'HH', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_cy, 'cy', 'household')
        await self.check_post_confirm_send_by_post_error_from_request_fulfilment(
            self.post_request_access_code_confirm_send_by_post_cy, 'cy')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_request_fulfilment_error_429_hh_ew_e(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'HH', 'E')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'household')
        await self.check_post_confirm_send_by_post_error_429_from_request_fulfilment_uac(
            self.post_request_access_code_confirm_send_by_post_en, 'en')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_request_fulfilment_error_429_hh_ew_w(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_en, 'en')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_en, 'en')
        await self.check_post_select_address(self.post_request_access_code_select_address_en, 'en', 'HH', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_en, 'en')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_en, 'en')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_en, 'en', 'household')
        await self.check_post_confirm_send_by_post_error_429_from_request_fulfilment_uac(
            self.post_request_access_code_confirm_send_by_post_en, 'en')

    @unittest_run_loop
    async def test_request_access_code_post_confirm_send_by_post_request_fulfilment_error_429_hh_cy(self):
        await self.check_get_enter_address(self.get_request_access_code_enter_address_cy, 'cy')
        await self.check_post_enter_address(self.post_request_access_code_enter_address_cy, 'cy')
        await self.check_post_select_address(self.post_request_access_code_select_address_cy, 'cy', 'HH', 'W')
        await self.check_post_confirm_address_input_yes_code(
            self.post_request_access_code_confirm_address_cy, 'cy')
        await self.check_post_select_how_to_receive_input_post(
            self.post_request_access_code_select_how_to_receive_cy, 'cy')
        await self.check_post_enter_name(self.post_request_access_code_enter_name_cy, 'cy', 'household')
        await self.check_post_confirm_send_by_post_error_429_from_request_fulfilment_uac(
            self.post_request_access_code_confirm_send_by_post_cy, 'cy')
