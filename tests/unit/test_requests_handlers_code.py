from unittest import mock

from aiohttp.client_exceptions import ClientConnectionError
from aiohttp.test_utils import unittest_run_loop
from aioresponses import aioresponses

from . import RHTestCase

attempts_retry_limit = 5


# noinspection PyTypeChecker
class TestRequestsHandlersAccessCode(RHTestCase):

    @unittest_run_loop
    async def test_request_access_code_sms_happy_path_hh_en(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment'
        ) as mocked_request_fulfilment:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_hh_e
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi
            mocked_request_fulfilment.return_value = self.rhsvc_request_fulfilment

            response = await self.client.request('GET',
                                                 self.get_request_access_code_enter_address_en)
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/enter-address'")
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_request_enter_address_title_en, contents)
            self.assertIn(self.content_request_enter_address_secondary_en, contents)

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'valid postcode')

            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/select-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn(self.content_common_select_address_title_en, str(resp_content))
            self.assertIn(self.content_common_select_address_value_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_en,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/confirm-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_title_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_yes_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_change_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_no_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/enter-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_title_en, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_secondary_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_mobile_en,
                    data=self.request_code_enter_mobile_form_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/enter-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/confirm-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_title_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_mobile_en,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/confirm-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/code-sent'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn(self.content_request_code_sent_title_en, str(resp_content))

    @unittest_run_loop
    async def test_request_access_code_sms_happy_path_hh_cy(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment'
        ) as mocked_request_fulfilment:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_hh_w
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi
            mocked_request_fulfilment.return_value = self.rhsvc_request_fulfilment

            response = await self.client.request('GET',
                                                 self.get_request_access_code_enter_address_cy)
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/access-code/enter-address'")
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn(self.content_request_enter_address_title_cy, contents)
            self.assertIn(self.content_request_enter_address_secondary_cy, contents)

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_cy,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'valid postcode')

            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/access-code/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/access-code/select-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn(self.content_common_select_address_title_cy, str(resp_content))
            self.assertIn(self.content_common_select_address_value_cy, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_cy,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/access-code/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/access-code/confirm-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn(self.content_common_confirm_address_title_cy, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_yes_cy, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_change_cy, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_no_cy, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_cy,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/access-code/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/access-code/enter-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_title_cy, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_secondary_cy, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_mobile_cy,
                    data=self.request_code_enter_mobile_form_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/access-code/enter-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/access-code/confirm-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_title_cy, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_mobile_cy,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/access-code/confirm-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/access-code/code-sent'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn(self.content_request_code_sent_title_cy, str(resp_content))

    @unittest_run_loop
    async def test_request_access_code_sms_happy_path_hh_ni(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment'
        ) as mocked_request_fulfilment:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_hh_n
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi
            mocked_request_fulfilment.return_value = self.rhsvc_request_fulfilment

            response = await self.client.request('GET',
                                                 self.get_request_access_code_enter_address_ni)
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/access-code/enter-address'")
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_request_enter_address_title_en, contents)
            self.assertIn(self.content_request_enter_address_secondary_en, contents)

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_ni,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'valid postcode')

            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/access-code/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/access-code/select-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_common_select_address_title_en, str(resp_content))
            self.assertIn(self.content_common_select_address_value_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_ni,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/access-code/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/access-code/confirm-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_common_confirm_address_title_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_yes_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_change_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_no_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_ni,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/access-code/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/access-code/enter-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_title_en, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_secondary_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_mobile_ni,
                    data=self.request_code_enter_mobile_form_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/access-code/enter-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/access-code/confirm-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_title_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_mobile_ni,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/access-code/confirm-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/access-code/code-sent'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_request_code_sent_title_en, str(resp_content))

    @unittest_run_loop
    async def test_request_access_code_sms_happy_path_spg_en(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment'
        ) as mocked_request_fulfilment:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_spg_e
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi
            mocked_request_fulfilment.return_value = self.rhsvc_request_fulfilment

            response = await self.client.request('GET',
                                                 self.get_request_access_code_enter_address_en)
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/enter-address'")
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_request_enter_address_title_en, contents)
            self.assertIn(self.content_request_enter_address_secondary_en, contents)

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'valid postcode')

            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/select-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn(self.content_common_select_address_title_en, str(resp_content))
            self.assertIn(self.content_common_select_address_value_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_en,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/confirm-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_title_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_yes_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_change_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_no_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/enter-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_title_en, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_secondary_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_mobile_en,
                    data=self.request_code_enter_mobile_form_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/enter-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/confirm-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_title_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_mobile_en,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/confirm-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/code-sent'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn(self.content_request_code_sent_title_en, str(resp_content))

    @unittest_run_loop
    async def test_request_access_code_sms_happy_path_spg_cy(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment'
        ) as mocked_request_fulfilment:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_spg_w
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi
            mocked_request_fulfilment.return_value = self.rhsvc_request_fulfilment

            response = await self.client.request('GET',
                                                 self.get_request_access_code_enter_address_cy)
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/access-code/enter-address'")
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn(self.content_request_enter_address_title_cy, contents)
            self.assertIn(self.content_request_enter_address_secondary_cy, contents)

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_cy,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'valid postcode')

            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/access-code/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/access-code/select-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn(self.content_common_select_address_title_cy, str(resp_content))
            self.assertIn(self.content_common_select_address_value_cy, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_cy,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/access-code/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/access-code/confirm-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn(self.content_common_confirm_address_title_cy, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_yes_cy, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_change_cy, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_no_cy, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_cy,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/access-code/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/access-code/enter-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_title_cy, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_secondary_cy, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_mobile_cy,
                    data=self.request_code_enter_mobile_form_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/access-code/enter-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/access-code/confirm-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_title_cy, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_mobile_cy,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/access-code/confirm-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/access-code/code-sent'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn(self.content_request_code_sent_title_cy, str(resp_content))

    @unittest_run_loop
    async def test_request_access_code_sms_happy_path_spg_ni(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment'
        ) as mocked_request_fulfilment:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_spg_n
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi
            mocked_request_fulfilment.return_value = self.rhsvc_request_fulfilment

            response = await self.client.request('GET',
                                                 self.get_request_access_code_enter_address_ni)
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/access-code/enter-address'")
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_request_enter_address_title_en, contents)
            self.assertIn(self.content_request_enter_address_secondary_en, contents)

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_ni,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'valid postcode')

            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/access-code/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/access-code/select-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_common_select_address_title_en, str(resp_content))
            self.assertIn(self.content_common_select_address_value_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_ni,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/access-code/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/access-code/confirm-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_common_confirm_address_title_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_yes_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_change_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_no_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_ni,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/access-code/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/access-code/enter-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_title_en, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_secondary_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_mobile_ni,
                    data=self.request_code_enter_mobile_form_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/access-code/enter-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/access-code/confirm-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_title_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_mobile_ni,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/access-code/confirm-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/access-code/code-sent'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_request_code_sent_title_en, str(resp_content))

    @unittest_run_loop
    async def test_request_access_code_sms_happy_path_ce_m_en(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment'
        ) as mocked_request_fulfilment:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_m_e
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi
            mocked_request_fulfilment.return_value = self.rhsvc_request_fulfilment

            response = await self.client.request('GET',
                                                 self.get_request_access_code_enter_address_en)
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/enter-address'")
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_request_enter_address_title_en, contents)
            self.assertIn(self.content_request_enter_address_secondary_en, contents)

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'valid postcode')

            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/select-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn(self.content_common_select_address_title_en, str(resp_content))
            self.assertIn(self.content_common_select_address_value_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_en,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/confirm-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_title_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_yes_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_change_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_no_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/enter-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_title_en, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_secondary_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_mobile_en,
                    data=self.request_code_enter_mobile_form_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/enter-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/confirm-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_title_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_mobile_en,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/confirm-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/code-sent'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn(self.content_request_code_sent_title_en, str(resp_content))

    @unittest_run_loop
    async def test_request_access_code_sms_happy_path_ce_m_cy(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment'
        ) as mocked_request_fulfilment:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_m_w
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi
            mocked_request_fulfilment.return_value = self.rhsvc_request_fulfilment

            response = await self.client.request('GET',
                                                 self.get_request_access_code_enter_address_cy)
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/access-code/enter-address'")
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn(self.content_request_enter_address_title_cy, contents)
            self.assertIn(self.content_request_enter_address_secondary_cy, contents)

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_cy,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'valid postcode')

            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/access-code/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/access-code/select-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn(self.content_common_select_address_title_cy, str(resp_content))
            self.assertIn(self.content_common_select_address_value_cy, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_cy,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/access-code/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/access-code/confirm-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn(self.content_common_confirm_address_title_cy, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_yes_cy, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_change_cy, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_no_cy, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_cy,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/access-code/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/access-code/enter-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_title_cy, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_secondary_cy, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_mobile_cy,
                    data=self.request_code_enter_mobile_form_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/access-code/enter-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/access-code/confirm-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_title_cy, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_mobile_cy,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/access-code/confirm-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/access-code/code-sent'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn(self.content_request_code_sent_title_cy, str(resp_content))

    @unittest_run_loop
    async def test_request_access_code_sms_happy_path_ce_m_ni(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment'
        ) as mocked_request_fulfilment:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_m_n
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi
            mocked_request_fulfilment.return_value = self.rhsvc_request_fulfilment

            response = await self.client.request('GET',
                                                 self.get_request_access_code_enter_address_ni)
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/access-code/enter-address'")
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_request_enter_address_title_en, contents)
            self.assertIn(self.content_request_enter_address_secondary_en, contents)

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_ni,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'valid postcode')

            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/access-code/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/access-code/select-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_common_select_address_title_en, str(resp_content))
            self.assertIn(self.content_common_select_address_value_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_ni,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/access-code/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/access-code/confirm-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_common_confirm_address_title_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_yes_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_change_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_no_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_ni,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/access-code/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/access-code/enter-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_title_en, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_secondary_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_mobile_ni,
                    data=self.request_code_enter_mobile_form_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/access-code/enter-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/access-code/confirm-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_title_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_mobile_ni,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/access-code/confirm-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/access-code/code-sent'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_request_code_sent_title_en, str(resp_content))

    @unittest_run_loop
    async def test_request_access_code_sms_happy_path_ce_r_en(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment'
        ) as mocked_request_fulfilment:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_r_e
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi
            mocked_request_fulfilment.return_value = self.rhsvc_request_fulfilment

            response = await self.client.request('GET',
                                                 self.get_request_access_code_enter_address_en)
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/enter-address'")
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_request_enter_address_title_en, contents)
            self.assertIn(self.content_request_enter_address_secondary_en, contents)

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'valid postcode')

            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/select-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn(self.content_common_select_address_title_en, str(resp_content))
            self.assertIn(self.content_common_select_address_value_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_en,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/confirm-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_title_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_yes_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_change_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_no_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/enter-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_title_en, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_secondary_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_mobile_en,
                    data=self.request_code_enter_mobile_form_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/enter-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/confirm-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_title_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_mobile_en,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/confirm-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/code-sent'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn(self.content_request_code_sent_title_en, str(resp_content))

    @unittest_run_loop
    async def test_request_access_code_sms_happy_path_ce_r_cy(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment'
        ) as mocked_request_fulfilment:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_r_w
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi
            mocked_request_fulfilment.return_value = self.rhsvc_request_fulfilment

            response = await self.client.request('GET',
                                                 self.get_request_access_code_enter_address_cy)
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/access-code/enter-address'")
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn(self.content_request_enter_address_title_cy, contents)
            self.assertIn(self.content_request_enter_address_secondary_cy, contents)

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_cy,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'valid postcode')

            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/access-code/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/access-code/select-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn(self.content_common_select_address_title_cy, str(resp_content))
            self.assertIn(self.content_common_select_address_value_cy, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_cy,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/access-code/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/access-code/confirm-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn(self.content_common_confirm_address_title_cy, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_yes_cy, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_change_cy, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_no_cy, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_cy,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/access-code/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/access-code/enter-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_title_cy, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_secondary_cy, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_mobile_cy,
                    data=self.request_code_enter_mobile_form_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/access-code/enter-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/access-code/confirm-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_title_cy, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_mobile_cy,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/access-code/confirm-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/access-code/code-sent'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn(self.content_request_code_sent_title_cy, str(resp_content))

    @unittest_run_loop
    async def test_request_access_code_sms_happy_path_ce_r_ni(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment'
        ) as mocked_request_fulfilment:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_ce_r_n
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi
            mocked_request_fulfilment.return_value = self.rhsvc_request_fulfilment

            response = await self.client.request('GET',
                                                 self.get_request_access_code_enter_address_ni)
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/access-code/enter-address'")
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_request_enter_address_title_en, contents)
            self.assertIn(self.content_request_enter_address_secondary_en, contents)

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_ni,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'valid postcode')

            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/access-code/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/access-code/select-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_common_select_address_title_en, str(resp_content))
            self.assertIn(self.content_common_select_address_value_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_ni,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/access-code/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/access-code/confirm-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_common_confirm_address_title_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_yes_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_change_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_no_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_ni,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/access-code/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/access-code/enter-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_title_en, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_secondary_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_mobile_ni,
                    data=self.request_code_enter_mobile_form_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/access-code/enter-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/access-code/confirm-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_title_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_mobile_ni,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/access-code/confirm-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/access-code/code-sent'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_request_code_sent_title_en, str(resp_content))

    @unittest_run_loop
    async def test_post_request_access_code_enter_address_not_found_en(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, \
                mock.patch('app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode:

            mocked_get_ai_postcode.return_value = self.ai_postcode_no_results

            response = await self.client.request(
                'POST',
                self.post_request_access_code_enter_address_en,
                data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'valid postcode')

            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/select-address'")

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_common_select_address_no_results_en, contents)

    @unittest_run_loop
    async def test_post_request_access_code_enter_address_not_found_cy(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, \
                mock.patch('app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode:

            mocked_get_ai_postcode.return_value = self.ai_postcode_no_results

            response = await self.client.request(
                'POST',
                self.post_request_access_code_enter_address_cy,
                data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'valid postcode')

            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/access-code/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/access-code/select-address'")

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn(self.content_common_select_address_no_results_cy, contents)

    @unittest_run_loop
    async def test_post_request_access_code_enter_address_not_found_ni(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, \
                mock.patch('app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode:

            mocked_get_ai_postcode.return_value = self.ai_postcode_no_results

            response = await self.client.request(
                'POST',
                self.post_request_access_code_enter_address_ni,
                data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'valid postcode')

            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/access-code/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/access-code/select-address'")

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_common_select_address_no_results_en, contents)

    @unittest_run_loop
    async def test_post_request_access_code_get_ai_postcode_connection_error_en(
            self):
        with self.assertLogs('respondent-home', 'WARN') as cm, \
                aioresponses(passthrough=[str(self.server._root)]) as mocked:

            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       exception=ClientConnectionError('Failed'))

            response = await self.client.request(
                'POST',
                self.post_request_access_code_enter_address_en,
                data=self.common_postcode_input_valid)

            self.assertLogEvent(cm,
                                'client failed to connect',
                                url=self.addressindexsvc_url +
                                self.postcode_valid +
                                self.address_index_epoch_param)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_post_request_access_code_get_ai_postcode_connection_error_cy(
            self):
        with self.assertLogs('respondent-home', 'WARN') as cm, \
                aioresponses(passthrough=[str(self.server._root)]) as mocked:

            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       exception=ClientConnectionError('Failed'))

            response = await self.client.request(
                'POST',
                self.post_request_access_code_enter_address_cy,
                data=self.common_postcode_input_valid)

            self.assertLogEvent(cm,
                                'client failed to connect',
                                url=self.addressindexsvc_url +
                                self.postcode_valid +
                                self.address_index_epoch_param)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn(self.content_common_500_error_cy, contents)

    @unittest_run_loop
    async def test_post_request_access_code_get_ai_postcode_connection_error_ni(
            self):
        with self.assertLogs('respondent-home', 'WARN') as cm, \
                aioresponses(passthrough=[str(self.server._root)]) as mocked:

            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       exception=ClientConnectionError('Failed'))

            response = await self.client.request(
                'POST',
                self.post_request_access_code_enter_address_ni,
                data=self.common_postcode_input_valid)

            self.assertLogEvent(cm,
                                'client failed to connect',
                                url=self.addressindexsvc_url +
                                self.postcode_valid +
                                self.address_index_epoch_param)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_post_request_access_code_get_ai_postcode_connection_error_with_epoch_en(
            self):
        with self.assertLogs('respondent-home', 'WARN') as cm, \
                aioresponses(passthrough=[str(self.server._root)]) as mocked:

            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       exception=ClientConnectionError('Failed'))
            self.app['ADDRESS_INDEX_EPOCH'] = 'test'

            response = await self.client.request(
                'POST',
                self.post_request_access_code_enter_address_en,
                data=self.common_postcode_input_valid)

            self.assertLogEvent(cm,
                                'client failed to connect',
                                url=self.addressindexsvc_url +
                                self.postcode_valid +
                                self.address_index_epoch_param_test)

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_post_request_access_code_get_ai_postcode_connection_error_with_epoch_cy(
            self):
        with self.assertLogs('respondent-home', 'WARN') as cm, \
                aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       exception=ClientConnectionError('Failed'))
            self.app['ADDRESS_INDEX_EPOCH'] = 'test'

            response = await self.client.request(
                'POST',
                self.post_request_access_code_enter_address_cy,
                data=self.common_postcode_input_valid)

            self.assertLogEvent(cm,
                                'client failed to connect',
                                url=self.addressindexsvc_url +
                                self.postcode_valid +
                                self.address_index_epoch_param_test)

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_cy, contents)
        self.assertIn(self.content_common_500_error_cy, contents)

    @unittest_run_loop
    async def test_post_request_access_code_get_ai_postcode_connection_error_with_epoch_ni(
            self):
        with self.assertLogs('respondent-home', 'WARN') as cm, \
                aioresponses(passthrough=[str(self.server._root)]) as mocked:

            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       exception=ClientConnectionError('Failed'))
            self.app['ADDRESS_INDEX_EPOCH'] = 'test'

            response = await self.client.request(
                'POST',
                self.post_request_access_code_enter_address_ni,
                data=self.common_postcode_input_valid)

            self.assertLogEvent(cm,
                                'client failed to connect',
                                url=self.addressindexsvc_url +
                                self.postcode_valid +
                                self.address_index_epoch_param_test)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_get_request_access_code_address_in_scotland_en(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result_scotland

            await self.client.request('GET', self.get_request_access_code_enter_address_en)
            await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_address_en,
                    data=self.common_postcode_input_valid)

            response_get_confirm = await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_en,
                    data=self.common_select_address_input_valid)
            resp_content = await response_get_confirm.content.read()
            self.assertIn(self.content_common_confirm_address_value_yes_en, str(resp_content))
            self.assertNotIn(self.content_common_confirm_address_value_change_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_no_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/address-in-scotland'")
            self.assertEqual(response.status, 200)

            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_common_address_in_scotland_en, contents)

    @unittest_run_loop
    async def test_get_request_access_code_address_in_scotland_cy(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result_scotland

            await self.client.request('GET', self.get_request_access_code_enter_address_cy)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_cy,
                    data=self.common_postcode_input_valid)

            response_get_confirm = await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_cy,
                    data=self.common_select_address_input_valid)
            resp_content = await response_get_confirm.content.read()
            self.assertIn(self.content_common_confirm_address_value_yes_cy, str(resp_content))
            self.assertNotIn(self.content_common_confirm_address_value_change_cy, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_no_cy, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_cy,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/access-code/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/address-in-scotland'")
            self.assertEqual(response.status, 200)

            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn(self.content_common_address_in_scotland_cy, contents)

    @unittest_run_loop
    async def test_get_request_access_code_address_in_scotland_ni(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result_scotland

            await self.client.request('GET', self.get_request_access_code_enter_address_ni)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_ni,
                    data=self.common_postcode_input_valid)

            response_get_confirm = await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_ni,
                    data=self.common_select_address_input_valid)
            resp_content = await response_get_confirm.content.read()
            self.assertIn(self.content_common_confirm_address_value_yes_en, str(resp_content))
            self.assertNotIn(self.content_common_confirm_address_value_change_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_no_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_ni,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/access-code/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/address-in-scotland'")
            self.assertEqual(response.status, 200)

            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_common_address_in_scotland_en, contents)

    @unittest_run_loop
    async def test_get_request_access_code_address_not_found_en(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            await self.client.request('GET', self.get_request_access_code_enter_address_en)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_en,
                    data=self.common_postcode_input_valid)
            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_en,
                    data=self.common_select_address_input_not_listed_en)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/call-contact-centre/address-not-found'")
            self.assertEqual(response.status, 200)

            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_common_call_contact_centre_address_not_found_title_en, contents)

    @unittest_run_loop
    async def test_get_request_access_code_address_not_found_cy(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            await self.client.request('GET', self.get_request_access_code_enter_address_cy)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_cy,
                    data=self.common_postcode_input_valid)
            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_cy,
                    data=self.common_select_address_input_not_listed_cy)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/access-code/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/call-contact-centre/address-not-found'")
            self.assertEqual(response.status, 200)

            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn(self.content_common_call_contact_centre_address_not_found_title_cy, contents)

    @unittest_run_loop
    async def test_get_request_access_code_address_not_found_ni(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            await self.client.request('GET', self.get_request_access_code_enter_address_ni)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_ni,
                    data=self.common_postcode_input_valid)
            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_ni,
                    data=self.common_select_address_input_not_listed_en)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/access-code/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/call-contact-centre/address-not-found'")
            self.assertEqual(response.status, 200)

            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_common_call_contact_centre_address_not_found_title_en, contents)

    @unittest_run_loop
    async def test_get_request_access_code_census_address_type_na_en(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result_censusaddresstype_na

            await self.client.request('GET', self.get_request_access_code_enter_address_en)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_en,
                    data=self.common_postcode_input_valid)

            response_get_confirm = await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_en,
                    data=self.common_select_address_input_valid)
            resp_content = await response_get_confirm.content.read()
            self.assertIn(self.content_common_confirm_address_value_yes_en, str(resp_content))
            self.assertNotIn(self.content_common_confirm_address_value_change_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_no_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/confirm-address'")
            self.assertLogEvent(cm,
                                "received GET on endpoint 'en/requests/call-contact-centre/unable-to-match-address'")

            self.assertEqual(200, response.status)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn(self.content_common_call_contact_centre_title_en, str(resp_content))
            self.assertIn(self.content_common_call_contact_centre_unable_to_match_address_en, str(resp_content))

    @unittest_run_loop
    async def test_get_request_access_code_census_address_type_na_cy(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result_censusaddresstype_na

            await self.client.request('GET', self.get_request_access_code_enter_address_cy)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_cy,
                    data=self.common_postcode_input_valid)

            response_get_confirm = await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_cy,
                    data=self.common_select_address_input_valid)
            resp_content = await response_get_confirm.content.read()
            self.assertIn(self.content_common_confirm_address_value_yes_cy, str(resp_content))
            self.assertNotIn(self.content_common_confirm_address_value_change_cy, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_no_cy, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_cy,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/access-code/confirm-address'")
            self.assertLogEvent(cm,
                                "received GET on endpoint 'cy/requests/call-contact-centre/unable-to-match-address'")

            self.assertEqual(200, response.status)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn(self.content_common_call_contact_centre_title_cy, str(resp_content))
            self.assertIn(self.content_common_call_contact_centre_unable_to_match_address_cy, str(resp_content))

    @unittest_run_loop
    async def test_get_request_access_code_census_address_type_na_ni(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result_censusaddresstype_na

            await self.client.request('GET', self.get_request_access_code_enter_address_ni)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_ni,
                    data=self.common_postcode_input_valid)

            response_get_confirm = await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_ni,
                    data=self.common_select_address_input_valid)
            resp_content = await response_get_confirm.content.read()
            self.assertIn(self.content_common_confirm_address_value_yes_en, str(resp_content))
            self.assertNotIn(self.content_common_confirm_address_value_change_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_no_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_ni,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/access-code/confirm-address'")
            self.assertLogEvent(cm,
                                "received GET on endpoint 'ni/requests/call-contact-centre/unable-to-match-address'")

            self.assertEqual(200, response.status)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_common_call_contact_centre_title_en, str(resp_content))
            self.assertIn(self.content_common_call_contact_centre_unable_to_match_address_en, str(resp_content))

    @unittest_run_loop
    async def test_get_request_access_code_confirm_address_data_change_en(
            self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertEqual(response.status, 200)

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_en,
                    data=self.common_select_address_input_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_confirm:
                response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_en,
                    data=self.common_confirm_address_input_change)
            self.assertLogEvent(cm_confirm, "received POST on endpoint 'en/requests/access-code/confirm-address'")
            self.assertLogEvent(cm_confirm,
                                "received GET on endpoint 'en/requests/call-contact-centre/address-not-found'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn(self.content_common_call_contact_centre_address_not_found_title_en, str(resp_content))
            self.assertIn(self.content_common_call_contact_centre_address_not_found_text_en, str(resp_content))

    @unittest_run_loop
    async def test_get_request_access_code_confirm_address_data_change_cy(
            self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_cy,
                    data=self.common_postcode_input_valid)
            self.assertEqual(response.status, 200)

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_cy,
                    data=self.common_select_address_input_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_confirm:
                response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_cy,
                    data=self.common_confirm_address_input_change)
            self.assertLogEvent(cm_confirm, "received POST on endpoint 'cy/requests/access-code/confirm-address'")
            self.assertLogEvent(cm_confirm,
                                "received GET on endpoint 'cy/requests/call-contact-centre/address-not-found'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn(self.content_common_call_contact_centre_address_not_found_title_cy, str(resp_content))
            self.assertIn(self.content_common_call_contact_centre_address_not_found_text_cy, str(resp_content))

    @unittest_run_loop
    async def test_get_request_access_code_confirm_address_data_change_ni(
            self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_ni,
                    data=self.common_postcode_input_valid)
            self.assertEqual(response.status, 200)

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_ni,
                    data=self.common_select_address_input_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_confirm:
                response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_ni,
                    data=self.common_confirm_address_input_change)
            self.assertLogEvent(cm_confirm, "received POST on endpoint 'ni/requests/access-code/confirm-address'")
            self.assertLogEvent(cm_confirm,
                                "received GET on endpoint 'ni/requests/call-contact-centre/address-not-found'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_common_call_contact_centre_address_not_found_title_en, str(resp_content))
            self.assertIn(self.content_common_call_contact_centre_address_not_found_text_en, str(resp_content))

    @unittest_run_loop
    async def test_post_request_access_code_enter_address_bad_postcode_en(
            self):

        with self.assertLogs('respondent-home', 'INFO') as cm:

            await self.client.request('GET', self.get_request_access_code_enter_address_en)
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/enter-address'")

            response = await self.client.request(
                'POST',
                self.post_request_access_code_enter_address_en,
                data=self.common_postcode_input_invalid)
        self.assertLogEvent(cm, 'invalid postcode')
        self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/enter-address'")

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertIn(self.content_request_enter_address_title_en, contents)
        self.assertIn(self.content_common_enter_address_error_en, contents)
        self.assertIn(self.content_request_enter_address_secondary_en, contents)

    @unittest_run_loop
    async def test_post_request_access_code_enter_address_bad_postcode_cy(
            self):

        with self.assertLogs('respondent-home', 'INFO') as cm:

            await self.client.request('GET', self.get_request_access_code_enter_address_cy)
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/access-code/enter-address'")

            response = await self.client.request(
                'POST',
                self.post_request_access_code_enter_address_cy,
                data=self.common_postcode_input_invalid)
        self.assertLogEvent(cm, 'invalid postcode')
        self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/access-code/enter-address'")

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_cy, contents)
        self.assertIn(self.content_request_enter_address_title_cy, contents)
        self.assertIn(self.content_common_enter_address_error_cy, contents)
        self.assertIn(self.content_request_enter_address_secondary_cy, contents)

    @unittest_run_loop
    async def test_post_request_access_code_enter_address_bad_postcode_ni(
            self):

        with self.assertLogs('respondent-home', 'INFO') as cm:

            await self.client.request('GET', self.get_request_access_code_enter_address_ni)
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/access-code/enter-address'")

            response = await self.client.request(
                'POST',
                self.post_request_access_code_enter_address_ni,
                data=self.common_postcode_input_invalid)
        self.assertLogEvent(cm, 'invalid postcode')
        self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/access-code/enter-address'")

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.nisra_logo, contents)
        self.assertIn(self.content_request_enter_address_title_en, contents)
        self.assertIn(self.content_common_enter_address_error_en, contents)
        self.assertIn(self.content_request_enter_address_secondary_en, contents)

    @unittest_run_loop
    async def test_get_request_access_code_timeout_en(self):

        with self.assertLogs('respondent-home', 'INFO') as cm:

            response = await self.client.request('GET',
                                                 self.get_request_access_code_timeout_en)
        self.assertLogEvent(cm, "received GET on endpoint 'en/requests/access-code/timeout'")
        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertIn(self.content_common_timeout_en, contents)
        self.assertIn(self.content_request_timeout_error_en, contents)

    @unittest_run_loop
    async def test_get_request_access_code_timeout_cy(self):

        with self.assertLogs('respondent-home', 'INFO') as cm:

            response = await self.client.request('GET',
                                                 self.get_request_access_code_timeout_cy)
        self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/access-code/timeout'")
        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.content_common_timeout_cy, contents)
        self.assertIn(self.content_request_timeout_error_cy, contents)

    @unittest_run_loop
    async def test_get_request_access_code_timeout_ni(self):

        with self.assertLogs('respondent-home', 'INFO') as cm:

            response = await self.client.request('GET',
                                                 self.get_request_access_code_timeout_ni)
        self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/access-code/timeout'")
        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.nisra_logo, contents)
        self.assertIn(self.content_common_timeout_en, contents)
        self.assertIn(self.content_request_timeout_error_en, contents)

    @unittest_run_loop
    async def test_get_request_access_code_confirm_address_get_cases_error_en(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, aioresponses(
            passthrough=[str(self.server._root)]
        ) as mocked_get_case_by_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.get(self.rhsvc_cases_by_uprn_url + self.selected_uprn, status=400)

            await self.client.request('GET', self.get_request_access_code_enter_address_en)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_en,
                    data=self.common_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_en,
                    data=self.common_select_address_input_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/confirm-address'")

            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_get_request_access_code_confirm_address_get_cases_error_cy(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, aioresponses(
            passthrough=[str(self.server._root)]
        ) as mocked_get_case_by_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.get(self.rhsvc_cases_by_uprn_url + self.selected_uprn, status=400)

            await self.client.request('GET', self.get_request_access_code_enter_address_cy)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_cy,
                    data=self.common_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_cy,
                    data=self.common_select_address_input_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_cy,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/access-code/confirm-address'")

            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn(self.content_common_500_error_cy, contents)

    @unittest_run_loop
    async def test_get_request_access_code_confirm_address_get_cases_error_ni(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, aioresponses(
            passthrough=[str(self.server._root)]
        ) as mocked_get_case_by_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.get(self.rhsvc_cases_by_uprn_url + self.selected_uprn, status=400)

            await self.client.request('GET', self.get_request_access_code_enter_address_ni)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_ni,
                    data=self.common_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_ni,
                    data=self.common_select_address_input_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_ni,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/access-code/confirm-address'")

            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_get_request_access_address_not_required_en(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, aioresponses(
            passthrough=[str(self.server._root)]
        ) as mocked_get_case_by_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.get(self.rhsvc_cases_by_uprn_url + self.selected_uprn, status=404)

            await self.client.request('GET', self.get_request_access_code_enter_address_en)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_en,
                    data=self.common_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_en,
                    data=self.common_select_address_input_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/access-code/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint "
                                    "'en/requests/call-contact-centre/unable-to-match-address'")
            self.assertEqual(response.status, 200)

            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_request_contact_centre_en, contents)

    @unittest_run_loop
    async def test_get_request_access_address_not_required_cy(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, aioresponses(
            passthrough=[str(self.server._root)]
        ) as mocked_get_case_by_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.get(self.rhsvc_cases_by_uprn_url + self.selected_uprn, status=404)

            await self.client.request('GET', self.get_request_access_code_enter_address_cy)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_cy,
                    data=self.common_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_cy,
                    data=self.common_select_address_input_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_cy,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/access-code/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint "
                                    "'cy/requests/call-contact-centre/unable-to-match-address'")
            self.assertEqual(response.status, 200)

            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn(self.content_request_contact_centre_cy, contents)

    @unittest_run_loop
    async def test_get_request_access_address_not_required_ni(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, aioresponses(
            passthrough=[str(self.server._root)]
        ) as mocked_get_case_by_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.get(self.rhsvc_cases_by_uprn_url + self.selected_uprn, status=404)

            await self.client.request('GET', self.get_request_access_code_enter_address_ni)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_ni,
                    data=self.common_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_ni,
                    data=self.common_select_address_input_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_ni,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/access-code/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint "
                                    "'ni/requests/call-contact-centre/unable-to-match-address'")
            self.assertEqual(response.status, 200)

            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_request_contact_centre_en, contents)

    @unittest_run_loop
    async def test_get_request_access_code_confirm_address_data_no_en(
            self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertEqual(response.status, 200)

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_en,
                    data=self.common_select_address_input_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_confirm:
                response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_en,
                    data=self.common_confirm_address_input_no)
            self.assertLogEvent(cm_confirm, "received POST on endpoint 'en/requests/access-code/confirm-address'")
            self.assertLogEvent(cm_confirm, "received GET on endpoint 'en/requests/access-code/enter-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn(self.content_request_enter_address_title_en, str(resp_content))
            self.assertIn(self.content_request_enter_address_secondary_en, str(resp_content))

    @unittest_run_loop
    async def test_get_request_access_code_confirm_address_data_no_cy(
            self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_cy,
                    data=self.common_postcode_input_valid)
            self.assertEqual(response.status, 200)

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_cy,
                    data=self.common_select_address_input_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_confirm:
                response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_cy,
                    data=self.common_confirm_address_input_no)
            self.assertLogEvent(cm_confirm, "received POST on endpoint 'cy/requests/access-code/confirm-address'")
            self.assertLogEvent(cm_confirm, "received GET on endpoint 'cy/requests/access-code/enter-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn(self.content_request_enter_address_title_cy, str(resp_content))
            self.assertIn(self.content_request_enter_address_secondary_cy, str(resp_content))

    @unittest_run_loop
    async def test_get_request_access_code_confirm_address_data_no_ni(
            self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_ni,
                    data=self.common_postcode_input_valid)
            self.assertEqual(response.status, 200)

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_ni,
                    data=self.common_select_address_input_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_confirm:
                response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_ni,
                    data=self.common_confirm_address_input_no)
            self.assertLogEvent(cm_confirm, "received POST on endpoint 'ni/requests/access-code/confirm-address'")
            self.assertLogEvent(cm_confirm, "received GET on endpoint 'ni/requests/access-code/enter-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_request_enter_address_title_en, str(resp_content))
            self.assertIn(self.content_request_enter_address_secondary_en, str(resp_content))

    @unittest_run_loop
    async def test_get_request_access_code_confirm_address_data_invalid_en(
            self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertEqual(response.status, 200)

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_en,
                    data=self.common_select_address_input_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_confirm:
                response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_en,
                    data=self.common_confirm_address_input_invalid)
            self.assertLogEvent(cm_confirm, "received POST on endpoint 'en/requests/access-code/confirm-address'")
            self.assertLogEvent(cm_confirm, "address confirmation error")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_title_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_error_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_yes_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_change_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_no_en, str(resp_content))

    @unittest_run_loop
    async def test_get_request_access_code_confirm_address_data_invalid_cy(
            self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_cy,
                    data=self.common_postcode_input_valid)
            self.assertEqual(response.status, 200)

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_cy,
                    data=self.common_select_address_input_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_confirm:
                response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_cy,
                    data=self.common_confirm_address_input_invalid)
            self.assertLogEvent(cm_confirm, "received POST on endpoint 'cy/requests/access-code/confirm-address'")
            self.assertLogEvent(cm_confirm, "address confirmation error")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn(self.content_common_confirm_address_title_cy, str(resp_content))
            self.assertIn(self.content_common_confirm_address_error_cy, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_yes_cy, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_change_cy, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_no_cy, str(resp_content))

    @unittest_run_loop
    async def test_get_request_access_code_confirm_address_data_invalid_ni(
            self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_ni,
                    data=self.common_postcode_input_valid)
            self.assertEqual(response.status, 200)

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_ni,
                    data=self.common_select_address_input_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_confirm:
                response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_ni,
                    data=self.common_confirm_address_input_invalid)
            self.assertLogEvent(cm_confirm, "received POST on endpoint 'ni/requests/access-code/confirm-address'")
            self.assertLogEvent(cm_confirm, "address confirmation error")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_common_confirm_address_title_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_error_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_yes_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_change_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_no_en, str(resp_content))

    @unittest_run_loop
    async def test_post_request_access_code_select_address_no_selection_en(
            self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_select:
                response = await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_en,
                    data=self.common_form_data_empty)
            self.assertLogEvent(cm_select, "received POST on endpoint 'en/requests/access-code/select-address'")
            self.assertLogEvent(cm_select, "no address selected")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn(self.content_common_select_address_title_en, str(resp_content))
            self.assertIn(self.content_common_select_address_error_en, str(resp_content))
            self.assertIn(self.content_common_select_address_value_en, str(resp_content))

    @unittest_run_loop
    async def test_post_request_access_code_select_address_no_selection_cy(
            self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_cy,
                    data=self.common_postcode_input_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_select:
                response = await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_cy,
                    data=self.common_form_data_empty)
            self.assertLogEvent(cm_select, "received POST on endpoint 'cy/requests/access-code/select-address'")
            self.assertLogEvent(cm_select, "no address selected")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn(self.content_common_select_address_title_cy, str(resp_content))
            self.assertIn(self.content_common_select_address_error_cy, str(resp_content))
            self.assertIn(self.content_common_select_address_value_cy, str(resp_content))

    @unittest_run_loop
    async def test_post_request_access_code_select_address_no_selection_ni(
            self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_ni,
                    data=self.common_postcode_input_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_select:
                response = await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_ni,
                    data=self.common_form_data_empty)
            self.assertLogEvent(cm_select, "received POST on endpoint 'ni/requests/access-code/select-address'")
            self.assertLogEvent(cm_select, "no address selected")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_common_select_address_title_en, str(resp_content))
            self.assertIn(self.content_common_select_address_error_en, str(resp_content))
            self.assertIn(self.content_common_select_address_value_en, str(resp_content))

    @unittest_run_loop
    async def test_get_request_access_code_confirm_address_no_selection_en(
            self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertEqual(response.status, 200)

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_en,
                    data=self.common_select_address_input_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_confirm:
                response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_en,
                    data=self.common_form_data_empty)
            self.assertLogEvent(cm_confirm, "received POST on endpoint 'en/requests/access-code/confirm-address'")
            self.assertLogEvent(cm_confirm, "address confirmation error")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_title_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_error_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_yes_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_change_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_no_en, str(resp_content))

    @unittest_run_loop
    async def test_get_request_access_code_confirm_address_no_selection_cy(
            self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_cy,
                    data=self.common_postcode_input_valid)
            self.assertEqual(response.status, 200)

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_cy,
                    data=self.common_select_address_input_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_confirm:
                response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_cy,
                    data=self.common_form_data_empty)
            self.assertLogEvent(cm_confirm, "received POST on endpoint 'cy/requests/access-code/confirm-address'")
            self.assertLogEvent(cm_confirm, "address confirmation error")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn(self.content_common_confirm_address_title_cy, str(resp_content))
            self.assertIn(self.content_common_confirm_address_error_cy, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_yes_cy, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_change_cy, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_no_cy, str(resp_content))

    @unittest_run_loop
    async def test_get_request_access_code_confirm_address_no_selection_ni(
            self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_ni,
                    data=self.common_postcode_input_valid)
            self.assertEqual(response.status, 200)

            response = await self.client.request(
                    'POST',
                    self.post_request_access_code_select_address_ni,
                    data=self.common_select_address_input_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_confirm:
                response = await self.client.request(
                    'POST',
                    self.post_request_access_code_confirm_address_ni,
                    data=self.common_form_data_empty)
            self.assertLogEvent(cm_confirm, "received POST on endpoint 'ni/requests/access-code/confirm-address'")
            self.assertLogEvent(cm_confirm, "address confirmation error")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_common_confirm_address_title_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_error_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_yes_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_change_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_no_en, str(resp_content))

    @unittest_run_loop
    async def test_post_request_access_code_get_ai_postcode_500_en(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       status=500)

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'error in response', status_code=500)

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_post_request_access_code_get_ai_postcode_500_cy(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       status=500)

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_cy,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'error in response', status_code=500)

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_cy, contents)
        self.assertIn(self.content_common_500_error_cy, contents)

    @unittest_run_loop
    async def test_post_request_access_code_get_ai_postcode_500_ni(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       status=500)

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_ni,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'error in response', status_code=500)

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.nisra_logo, contents)
        self.assertIn(self.content_common_500_error_en, contents)

    def mock503s(self, mocked, times):
        for i in range(times):
            mocked.get(self.addressindexsvc_url + self.postcode_valid, status=503)

    @unittest_run_loop
    async def test_post_request_access_code_get_ai_postcode_503_en(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            self.mock503s(mocked, attempts_retry_limit)

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'error in response', status_code=503)

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_post_request_access_code_get_ai_postcode_503_cy(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            self.mock503s(mocked, attempts_retry_limit)

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_cy,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'error in response', status_code=503)

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_cy, contents)
        self.assertIn(self.content_common_500_error_cy, contents)

    @unittest_run_loop
    async def test_post_request_access_code_get_ai_postcode_503_ni(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            self.mock503s(mocked, attempts_retry_limit)

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_ni,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'error in response', status_code=503)

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.nisra_logo, contents)
        self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_post_request_access_code_get_ai_postcode_403_en(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       status=403)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'error in response', status_code=403)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_post_request_access_code_get_ai_postcode_403_cy(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       status=403)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_cy,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'error in response', status_code=403)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn(self.content_common_500_error_cy,
                          contents)

    @unittest_run_loop
    async def test_post_request_access_code_get_ai_postcode_403_ni(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       status=403)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_ni,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'error in response', status_code=403)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_post_request_access_code_get_ai_postcode_401_en(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       status=401)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'error in response', status_code=401)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_post_request_access_code_get_ai_postcode_401_cy(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       status=401)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_cy,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'error in response', status_code=401)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn(self.content_common_500_error_cy,
                          contents)

    @unittest_run_loop
    async def test_post_request_access_code_get_ai_postcode_401_ni(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       status=401)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_ni,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'error in response', status_code=401)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_post_request_access_code_get_ai_postcode_400_en(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       status=400)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_post_request_access_code_get_ai_postcode_400_cy(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       status=400)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_cy,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn(self.content_common_500_error_cy,
                          contents)

    @unittest_run_loop
    async def test_post_request_access_code_get_ai_postcode_400_ni(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       status=400)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_request_access_code_enter_address_ni,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_common_500_error_en, contents)


# noinspection PyTypeChecker
class TestRequestsHandlersHouseholdCode(RHTestCase):

    @unittest_run_loop
    async def test_request_household_code_sms_happy_path_hh_en(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment'
        ) as mocked_request_fulfilment:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_hh_e
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi
            mocked_request_fulfilment.return_value = self.rhsvc_request_fulfilment

            response = await self.client.request('GET',
                                                 self.get_request_household_code_en)
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/household-code'")
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_request_household_title_en, contents)
            self.assertIn(self.content_request_secondary_en, contents)

            response = await self.client.request('GET',
                                                 self.get_request_household_code_enter_address_en)
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/household-code/enter-address'")
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_request_enter_address_title_en, contents)
            self.assertIn(self.content_request_enter_address_secondary_en, contents)

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'valid postcode')

            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/household-code/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/household-code/select-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn(self.content_common_select_address_title_en, str(resp_content))
            self.assertIn(self.content_common_select_address_value_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_select_address_en,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/household-code/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/household-code/confirm-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_title_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_yes_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_change_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_no_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/household-code/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/household-code/enter-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_title_en, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_secondary_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_mobile_en,
                    data=self.request_code_enter_mobile_form_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/household-code/enter-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/household-code/confirm-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_title_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_confirm_mobile_en,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/household-code/confirm-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/household-code/code-sent'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn(self.content_request_code_sent_title_en, str(resp_content))

    @unittest_run_loop
    async def test_request_household_code_sms_happy_path_hh_cy(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment'
        ) as mocked_request_fulfilment:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_hh_w
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi
            mocked_request_fulfilment.return_value = self.rhsvc_request_fulfilment

            response = await self.client.request('GET',
                                                 self.get_request_household_code_cy)
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/household-code'")
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn(self.content_request_household_title_cy, contents)
            self.assertIn(self.content_request_secondary_cy, contents)

            response = await self.client.request('GET',
                                                 self.get_request_household_code_enter_address_cy)
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/household-code/enter-address'")
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn(self.content_request_enter_address_title_cy, contents)
            self.assertIn(self.content_request_enter_address_secondary_cy, contents)

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_address_cy,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'valid postcode')

            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/household-code/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/household-code/select-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn(self.content_common_select_address_title_cy, str(resp_content))
            self.assertIn(self.content_common_select_address_value_cy, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_select_address_cy,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/household-code/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/household-code/confirm-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn(self.content_common_confirm_address_title_cy, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_yes_cy, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_change_cy, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_no_cy, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_confirm_address_cy,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/household-code/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/household-code/enter-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_title_cy, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_secondary_cy, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_mobile_cy,
                    data=self.request_code_enter_mobile_form_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/household-code/enter-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/household-code/confirm-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_title_cy, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_confirm_mobile_cy,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/household-code/confirm-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/household-code/code-sent'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn(self.content_request_code_sent_title_cy, str(resp_content))

    @unittest_run_loop
    async def test_request_household_code_sms_happy_path_hh_ni(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment'
        ) as mocked_request_fulfilment:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_hh_n
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi
            mocked_request_fulfilment.return_value = self.rhsvc_request_fulfilment

            response = await self.client.request('GET',
                                                 self.get_request_household_code_ni)
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/household-code'")
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_request_household_title_en, contents)
            self.assertIn(self.content_request_secondary_en, contents)

            response = await self.client.request('GET',
                                                 self.get_request_household_code_enter_address_ni)
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/household-code/enter-address'")
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_request_enter_address_title_en, contents)
            self.assertIn(self.content_request_enter_address_secondary_en, contents)

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_address_ni,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'valid postcode')

            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/household-code/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/household-code/select-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_common_select_address_title_en, str(resp_content))
            self.assertIn(self.content_common_select_address_value_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_select_address_ni,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/household-code/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/household-code/confirm-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_common_confirm_address_title_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_yes_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_change_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_no_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_confirm_address_ni,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/household-code/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/household-code/enter-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_title_en, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_secondary_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_mobile_ni,
                    data=self.request_code_enter_mobile_form_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/household-code/enter-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/household-code/confirm-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_title_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_confirm_mobile_ni,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/household-code/confirm-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/household-code/code-sent'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_request_code_sent_title_en, str(resp_content))

    @unittest_run_loop
    async def test_post_request_household_code_enter_address_not_found_en(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, \
                mock.patch('app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode:

            mocked_get_ai_postcode.return_value = self.ai_postcode_no_results

            response = await self.client.request(
                'POST',
                self.post_request_household_code_enter_address_en,
                data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'valid postcode')

            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/household-code/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/household-code/select-address'")

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_common_select_address_no_results_en, contents)

    @unittest_run_loop
    async def test_post_request_household_code_enter_address_not_found_cy(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, \
                mock.patch('app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode:

            mocked_get_ai_postcode.return_value = self.ai_postcode_no_results

            response = await self.client.request(
                'POST',
                self.post_request_household_code_enter_address_cy,
                data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'valid postcode')

            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/household-code/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/household-code/select-address'")

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn(self.content_common_select_address_no_results_cy, contents)

    @unittest_run_loop
    async def test_post_request_household_code_enter_address_not_found_ni(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, \
                mock.patch('app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode:

            mocked_get_ai_postcode.return_value = self.ai_postcode_no_results

            response = await self.client.request(
                'POST',
                self.post_request_household_code_enter_address_ni,
                data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'valid postcode')

            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/household-code/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/household-code/select-address'")

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_common_select_address_no_results_en, contents)

    @unittest_run_loop
    async def test_post_request_household_code_get_ai_postcode_connection_error_en(
            self):
        with self.assertLogs('respondent-home', 'WARN') as cm, \
                aioresponses(passthrough=[str(self.server._root)]) as mocked:

            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       exception=ClientConnectionError('Failed'))

            response = await self.client.request(
                'POST',
                self.post_request_household_code_enter_address_en,
                data=self.common_postcode_input_valid)

            self.assertLogEvent(cm,
                                'client failed to connect',
                                url=self.addressindexsvc_url +
                                self.postcode_valid +
                                self.address_index_epoch_param)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_post_request_household_code_get_ai_postcode_connection_error_cy(
            self):
        with self.assertLogs('respondent-home', 'WARN') as cm, \
                aioresponses(passthrough=[str(self.server._root)]) as mocked:

            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       exception=ClientConnectionError('Failed'))

            response = await self.client.request(
                'POST',
                self.post_request_household_code_enter_address_cy,
                data=self.common_postcode_input_valid)

            self.assertLogEvent(cm,
                                'client failed to connect',
                                url=self.addressindexsvc_url +
                                self.postcode_valid +
                                self.address_index_epoch_param)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn(self.content_common_500_error_cy, contents)

    @unittest_run_loop
    async def test_post_request_household_code_get_ai_postcode_connection_error_ni(
            self):
        with self.assertLogs('respondent-home', 'WARN') as cm, \
                aioresponses(passthrough=[str(self.server._root)]) as mocked:

            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       exception=ClientConnectionError('Failed'))

            response = await self.client.request(
                'POST',
                self.post_request_household_code_enter_address_ni,
                data=self.common_postcode_input_valid)

            self.assertLogEvent(cm,
                                'client failed to connect',
                                url=self.addressindexsvc_url +
                                self.postcode_valid +
                                self.address_index_epoch_param)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_post_request_household_code_get_ai_postcode_connection_error_with_epoch_en(
            self):
        with self.assertLogs('respondent-home', 'WARN') as cm, \
                aioresponses(passthrough=[str(self.server._root)]) as mocked:

            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       exception=ClientConnectionError('Failed'))
            self.app['ADDRESS_INDEX_EPOCH'] = 'test'

            response = await self.client.request(
                'POST',
                self.post_request_household_code_enter_address_en,
                data=self.common_postcode_input_valid)

            self.assertLogEvent(cm,
                                'client failed to connect',
                                url=self.addressindexsvc_url +
                                self.postcode_valid +
                                self.address_index_epoch_param_test)

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_post_request_household_code_get_ai_postcode_connection_error_with_epoch_cy(
            self):
        with self.assertLogs('respondent-home', 'WARN') as cm, \
                aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       exception=ClientConnectionError('Failed'))
            self.app['ADDRESS_INDEX_EPOCH'] = 'test'

            response = await self.client.request(
                'POST',
                self.post_request_household_code_enter_address_cy,
                data=self.common_postcode_input_valid)

            self.assertLogEvent(cm,
                                'client failed to connect',
                                url=self.addressindexsvc_url +
                                self.postcode_valid +
                                self.address_index_epoch_param_test)

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_cy, contents)
        self.assertIn(self.content_common_500_error_cy, contents)

    @unittest_run_loop
    async def test_post_request_household_code_get_ai_postcode_connection_error_with_epoch_ni(
            self):
        with self.assertLogs('respondent-home', 'WARN') as cm, \
                aioresponses(passthrough=[str(self.server._root)]) as mocked:

            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       exception=ClientConnectionError('Failed'))
            self.app['ADDRESS_INDEX_EPOCH'] = 'test'

            response = await self.client.request(
                'POST',
                self.post_request_household_code_enter_address_ni,
                data=self.common_postcode_input_valid)

            self.assertLogEvent(cm,
                                'client failed to connect',
                                url=self.addressindexsvc_url +
                                self.postcode_valid +
                                self.address_index_epoch_param_test)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_get_request_household_code_address_in_scotland_en(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result_scotland

            await self.client.request('GET', self.get_request_household_code_en)
            await self.client.request('GET', self.get_request_household_code_enter_address_en)
            await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_address_en,
                    data=self.common_postcode_input_valid)

            response_get_confirm = await self.client.request(
                    'POST',
                    self.post_request_household_code_select_address_en,
                    data=self.common_select_address_input_valid)
            resp_content = await response_get_confirm.content.read()
            self.assertIn(self.content_common_confirm_address_value_yes_en, str(resp_content))
            self.assertNotIn(self.content_common_confirm_address_value_change_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_no_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/household-code/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/address-in-scotland'")
            self.assertEqual(response.status, 200)

            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_common_address_in_scotland_en, contents)

    @unittest_run_loop
    async def test_get_request_household_code_address_in_scotland_cy(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result_scotland

            await self.client.request('GET', self.get_request_household_code_cy)
            await self.client.request('GET', self.get_request_household_code_enter_address_cy)
            await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_address_cy,
                    data=self.common_postcode_input_valid)

            response_get_confirm = await self.client.request(
                    'POST',
                    self.post_request_household_code_select_address_cy,
                    data=self.common_select_address_input_valid)
            resp_content = await response_get_confirm.content.read()
            self.assertIn(self.content_common_confirm_address_value_yes_cy, str(resp_content))
            self.assertNotIn(self.content_common_confirm_address_value_change_cy, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_no_cy, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_confirm_address_cy,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/household-code/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/address-in-scotland'")
            self.assertEqual(response.status, 200)

            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn(self.content_common_address_in_scotland_cy, contents)

    @unittest_run_loop
    async def test_get_request_household_code_address_in_scotland_ni(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result_scotland

            await self.client.request('GET', self.get_request_household_code_ni)
            await self.client.request('GET', self.get_request_household_code_enter_address_ni)
            await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_address_ni,
                    data=self.common_postcode_input_valid)

            response_get_confirm = await self.client.request(
                    'POST',
                    self.post_request_household_code_select_address_ni,
                    data=self.common_select_address_input_valid)
            resp_content = await response_get_confirm.content.read()
            self.assertIn(self.content_common_confirm_address_value_yes_en, str(resp_content))
            self.assertNotIn(self.content_common_confirm_address_value_change_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_no_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_confirm_address_ni,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/household-code/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/address-in-scotland'")
            self.assertEqual(response.status, 200)

            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_common_address_in_scotland_en, contents)

    @unittest_run_loop
    async def test_get_request_household_code_address_not_found_en(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            await self.client.request('GET', self.get_request_household_code_en)
            await self.client.request('GET', self.get_request_household_code_enter_address_en)
            await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_address_en,
                    data=self.common_postcode_input_valid)
            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_select_address_en,
                    data=self.common_select_address_input_not_listed_en)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/household-code/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/call-contact-centre/address-not-found'")
            self.assertEqual(response.status, 200)

            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_common_call_contact_centre_address_not_found_title_en, contents)

    @unittest_run_loop
    async def test_get_request_household_code_address_not_found_cy(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            await self.client.request('GET', self.get_request_household_code_cy)
            await self.client.request('GET', self.get_request_household_code_enter_address_cy)
            await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_address_cy,
                    data=self.common_postcode_input_valid)
            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_select_address_cy,
                    data=self.common_select_address_input_not_listed_cy)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/household-code/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/call-contact-centre/address-not-found'")
            self.assertEqual(response.status, 200)

            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn(self.content_common_call_contact_centre_address_not_found_title_cy, contents)

    @unittest_run_loop
    async def test_get_request_household_code_address_not_found_ni(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            await self.client.request('GET', self.get_request_household_code_ni)
            await self.client.request('GET', self.get_request_household_code_enter_address_ni)
            await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_address_ni,
                    data=self.common_postcode_input_valid)
            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_select_address_ni,
                    data=self.common_select_address_input_not_listed_en)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/household-code/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/call-contact-centre/address-not-found'")
            self.assertEqual(response.status, 200)

            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_common_call_contact_centre_address_not_found_title_en, contents)

    @unittest_run_loop
    async def test_get_request_household_code_census_address_type_na_en(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result_censusaddresstype_na

            await self.client.request('GET', self.get_request_household_code_en)
            await self.client.request('GET', self.get_request_household_code_enter_address_en)
            await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_address_en,
                    data=self.common_postcode_input_valid)

            response_get_confirm = await self.client.request(
                    'POST',
                    self.post_request_household_code_select_address_en,
                    data=self.common_select_address_input_valid)
            resp_content = await response_get_confirm.content.read()
            self.assertIn(self.content_common_confirm_address_value_yes_en, str(resp_content))
            self.assertNotIn(self.content_common_confirm_address_value_change_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_no_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/household-code/confirm-address'")
            self.assertLogEvent(cm,
                                "received GET on endpoint 'en/requests/call-contact-centre/unable-to-match-address'")

            self.assertEqual(200, response.status)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn(self.content_common_call_contact_centre_title_en, str(resp_content))
            self.assertIn(self.content_common_call_contact_centre_unable_to_match_address_en, str(resp_content))

    @unittest_run_loop
    async def test_get_request_household_code_census_address_type_na_cy(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result_censusaddresstype_na

            await self.client.request('GET', self.get_request_household_code_cy)
            await self.client.request('GET', self.get_request_household_code_enter_address_cy)
            await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_address_cy,
                    data=self.common_postcode_input_valid)

            response_get_confirm = await self.client.request(
                    'POST',
                    self.post_request_household_code_select_address_cy,
                    data=self.common_select_address_input_valid)
            resp_content = await response_get_confirm.content.read()
            self.assertIn(self.content_common_confirm_address_value_yes_cy, str(resp_content))
            self.assertNotIn(self.content_common_confirm_address_value_change_cy, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_no_cy, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_confirm_address_cy,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/household-code/confirm-address'")
            self.assertLogEvent(cm,
                                "received GET on endpoint 'cy/requests/call-contact-centre/unable-to-match-address'")

            self.assertEqual(200, response.status)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn(self.content_common_call_contact_centre_title_cy, str(resp_content))
            self.assertIn(self.content_common_call_contact_centre_unable_to_match_address_cy, str(resp_content))

    @unittest_run_loop
    async def test_get_request_household_code_census_address_type_na_ni(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result_censusaddresstype_na

            await self.client.request('GET', self.get_request_household_code_ni)
            await self.client.request('GET', self.get_request_household_code_enter_address_ni)
            await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_address_ni,
                    data=self.common_postcode_input_valid)

            response_get_confirm = await self.client.request(
                    'POST',
                    self.post_request_household_code_select_address_ni,
                    data=self.common_select_address_input_valid)
            resp_content = await response_get_confirm.content.read()
            self.assertIn(self.content_common_confirm_address_value_yes_en, str(resp_content))
            self.assertNotIn(self.content_common_confirm_address_value_change_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_no_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_confirm_address_ni,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/household-code/confirm-address'")
            self.assertLogEvent(cm,
                                "received GET on endpoint 'ni/requests/call-contact-centre/unable-to-match-address'")

            self.assertEqual(200, response.status)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_common_call_contact_centre_title_en, str(resp_content))
            self.assertIn(self.content_common_call_contact_centre_unable_to_match_address_en, str(resp_content))

    @unittest_run_loop
    async def test_get_request_household_code_confirm_address_data_change_en(
            self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertEqual(response.status, 200)

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_select_address_en,
                    data=self.common_select_address_input_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_confirm:
                response = await self.client.request(
                    'POST',
                    self.post_request_household_code_confirm_address_en,
                    data=self.common_confirm_address_input_change)
            self.assertLogEvent(cm_confirm, "received POST on endpoint 'en/requests/household-code/confirm-address'")
            self.assertLogEvent(cm_confirm,
                                "received GET on endpoint 'en/requests/call-contact-centre/address-not-found'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn(self.content_common_call_contact_centre_address_not_found_title_en, str(resp_content))
            self.assertIn(self.content_common_call_contact_centre_address_not_found_text_en, str(resp_content))

    @unittest_run_loop
    async def test_get_request_household_code_confirm_address_data_change_cy(
            self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_address_cy,
                    data=self.common_postcode_input_valid)
            self.assertEqual(response.status, 200)

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_select_address_cy,
                    data=self.common_select_address_input_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_confirm:
                response = await self.client.request(
                    'POST',
                    self.post_request_household_code_confirm_address_cy,
                    data=self.common_confirm_address_input_change)
            self.assertLogEvent(cm_confirm, "received POST on endpoint 'cy/requests/household-code/confirm-address'")
            self.assertLogEvent(cm_confirm,
                                "received GET on endpoint 'cy/requests/call-contact-centre/address-not-found'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn(self.content_common_call_contact_centre_address_not_found_title_cy, str(resp_content))
            self.assertIn(self.content_common_call_contact_centre_address_not_found_text_cy, str(resp_content))

    @unittest_run_loop
    async def test_get_request_household_code_confirm_address_data_change_ni(
            self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_address_ni,
                    data=self.common_postcode_input_valid)
            self.assertEqual(response.status, 200)

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_select_address_ni,
                    data=self.common_select_address_input_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_confirm:
                response = await self.client.request(
                    'POST',
                    self.post_request_household_code_confirm_address_ni,
                    data=self.common_confirm_address_input_change)
            self.assertLogEvent(cm_confirm, "received POST on endpoint 'ni/requests/household-code/confirm-address'")
            self.assertLogEvent(cm_confirm,
                                "received GET on endpoint 'ni/requests/call-contact-centre/address-not-found'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_common_call_contact_centre_address_not_found_title_en, str(resp_content))
            self.assertIn(self.content_common_call_contact_centre_address_not_found_text_en, str(resp_content))

    @unittest_run_loop
    async def test_post_request_household_code_enter_address_bad_postcode_en(
            self):

        with self.assertLogs('respondent-home', 'INFO') as cm:

            await self.client.request('GET', self.get_request_household_code_en)

            await self.client.request('GET', self.get_request_household_code_enter_address_en)
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/household-code/enter-address'")

            response = await self.client.request(
                'POST',
                self.post_request_household_code_enter_address_en,
                data=self.common_postcode_input_invalid)
        self.assertLogEvent(cm, 'invalid postcode')
        self.assertLogEvent(cm, "received POST on endpoint 'en/requests/household-code/enter-address'")

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertIn(self.content_request_enter_address_title_en, contents)
        self.assertIn(self.content_common_enter_address_error_en, contents)
        self.assertIn(self.content_request_enter_address_secondary_en, contents)

    @unittest_run_loop
    async def test_post_request_household_code_enter_address_bad_postcode_cy(
            self):

        with self.assertLogs('respondent-home', 'INFO') as cm:

            await self.client.request('GET', self.get_request_household_code_cy)

            await self.client.request('GET', self.get_request_household_code_enter_address_cy)
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/household-code/enter-address'")

            response = await self.client.request(
                'POST',
                self.post_request_household_code_enter_address_cy,
                data=self.common_postcode_input_invalid)
        self.assertLogEvent(cm, 'invalid postcode')
        self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/household-code/enter-address'")

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_cy, contents)
        self.assertIn(self.content_request_enter_address_title_cy, contents)
        self.assertIn(self.content_common_enter_address_error_cy, contents)
        self.assertIn(self.content_request_enter_address_secondary_cy, contents)

    @unittest_run_loop
    async def test_post_request_household_code_enter_address_bad_postcode_ni(
            self):

        with self.assertLogs('respondent-home', 'INFO') as cm:

            await self.client.request('GET', self.get_request_household_code_ni)

            await self.client.request('GET', self.get_request_household_code_enter_address_ni)
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/household-code/enter-address'")

            response = await self.client.request(
                'POST',
                self.post_request_household_code_enter_address_ni,
                data=self.common_postcode_input_invalid)
        self.assertLogEvent(cm, 'invalid postcode')
        self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/household-code/enter-address'")

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.nisra_logo, contents)
        self.assertIn(self.content_request_enter_address_title_en, contents)
        self.assertIn(self.content_common_enter_address_error_en, contents)
        self.assertIn(self.content_request_enter_address_secondary_en, contents)

    @unittest_run_loop
    async def test_get_request_household_code_timeout_en(self):

        with self.assertLogs('respondent-home', 'INFO') as cm:

            response = await self.client.request('GET',
                                                 self.get_request_household_code_timeout_en)
        self.assertLogEvent(cm, "received GET on endpoint 'en/requests/household-code/timeout'")
        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertIn(self.content_common_timeout_en, contents)
        self.assertIn(self.content_request_timeout_error_en, contents)

    @unittest_run_loop
    async def test_get_request_household_code_timeout_cy(self):

        with self.assertLogs('respondent-home', 'INFO') as cm:

            response = await self.client.request('GET',
                                                 self.get_request_household_code_timeout_cy)
        self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/household-code/timeout'")
        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.content_common_timeout_cy, contents)
        self.assertIn(self.content_request_timeout_error_cy, contents)

    @unittest_run_loop
    async def test_get_request_household_code_timeout_ni(self):

        with self.assertLogs('respondent-home', 'INFO') as cm:

            response = await self.client.request('GET',
                                                 self.get_request_household_code_timeout_ni)
        self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/household-code/timeout'")
        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.nisra_logo, contents)
        self.assertIn(self.content_common_timeout_en, contents)
        self.assertIn(self.content_request_timeout_error_en, contents)

    @unittest_run_loop
    async def test_get_request_household_code_confirm_address_get_cases_error_en(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, aioresponses(
            passthrough=[str(self.server._root)]
        ) as mocked_get_case_by_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.get(self.rhsvc_cases_by_uprn_url + self.selected_uprn, status=400)

            await self.client.request('GET', self.get_request_household_code_en)
            await self.client.request('GET', self.get_request_household_code_enter_address_en)
            await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_address_en,
                    data=self.common_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_household_code_select_address_en,
                    data=self.common_select_address_input_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/household-code/confirm-address'")

            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_get_request_household_code_confirm_address_get_cases_error_cy(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, aioresponses(
            passthrough=[str(self.server._root)]
        ) as mocked_get_case_by_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.get(self.rhsvc_cases_by_uprn_url + self.selected_uprn, status=400)

            await self.client.request('GET', self.get_request_household_code_cy)
            await self.client.request('GET', self.get_request_household_code_enter_address_cy)
            await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_address_cy,
                    data=self.common_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_household_code_select_address_cy,
                    data=self.common_select_address_input_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_confirm_address_cy,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/household-code/confirm-address'")

            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn(self.content_common_500_error_cy, contents)

    @unittest_run_loop
    async def test_get_request_household_code_confirm_address_get_cases_error_ni(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, aioresponses(
            passthrough=[str(self.server._root)]
        ) as mocked_get_case_by_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.get(self.rhsvc_cases_by_uprn_url + self.selected_uprn, status=400)

            await self.client.request('GET', self.get_request_household_code_ni)
            await self.client.request('GET', self.get_request_household_code_enter_address_ni)
            await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_address_ni,
                    data=self.common_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_household_code_select_address_ni,
                    data=self.common_select_address_input_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_confirm_address_ni,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/household-code/confirm-address'")

            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_get_request_household_address_not_required_en(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, aioresponses(
            passthrough=[str(self.server._root)]
        ) as mocked_get_case_by_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.get(self.rhsvc_cases_by_uprn_url + self.selected_uprn, status=404)

            await self.client.request('GET', self.get_request_household_code_en)
            await self.client.request('GET', self.get_request_household_code_enter_address_en)
            await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_address_en,
                    data=self.common_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_household_code_select_address_en,
                    data=self.common_select_address_input_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/household-code/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint "
                                    "'en/requests/call-contact-centre/unable-to-match-address'")
            self.assertEqual(response.status, 200)

            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_request_contact_centre_en, contents)

    @unittest_run_loop
    async def test_get_request_household_address_not_required_cy(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, aioresponses(
            passthrough=[str(self.server._root)]
        ) as mocked_get_case_by_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.get(self.rhsvc_cases_by_uprn_url + self.selected_uprn, status=404)

            await self.client.request('GET', self.get_request_household_code_cy)
            await self.client.request('GET', self.get_request_household_code_enter_address_cy)
            await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_address_cy,
                    data=self.common_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_household_code_select_address_cy,
                    data=self.common_select_address_input_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_confirm_address_cy,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/household-code/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint "
                                    "'cy/requests/call-contact-centre/unable-to-match-address'")
            self.assertEqual(response.status, 200)

            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn(self.content_request_contact_centre_cy, contents)

    @unittest_run_loop
    async def test_get_request_household_address_not_required_ni(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, aioresponses(
            passthrough=[str(self.server._root)]
        ) as mocked_get_case_by_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.get(self.rhsvc_cases_by_uprn_url + self.selected_uprn, status=404)

            await self.client.request('GET', self.get_request_household_code_ni)
            await self.client.request('GET', self.get_request_household_code_enter_address_ni)
            await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_address_ni,
                    data=self.common_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_household_code_select_address_ni,
                    data=self.common_select_address_input_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_confirm_address_ni,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/household-code/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint "
                                    "'ni/requests/call-contact-centre/unable-to-match-address'")
            self.assertEqual(response.status, 200)

            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_request_contact_centre_en, contents)

    @unittest_run_loop
    async def test_get_request_household_code_confirm_address_data_no_en(
            self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertEqual(response.status, 200)

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_select_address_en,
                    data=self.common_select_address_input_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_confirm:
                response = await self.client.request(
                    'POST',
                    self.post_request_household_code_confirm_address_en,
                    data=self.common_confirm_address_input_no)
            self.assertLogEvent(cm_confirm, "received POST on endpoint 'en/requests/household-code/confirm-address'")
            self.assertLogEvent(cm_confirm, "received GET on endpoint 'en/requests/household-code/enter-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn(self.content_request_enter_address_title_en, str(resp_content))
            self.assertIn(self.content_request_enter_address_secondary_en, str(resp_content))

    @unittest_run_loop
    async def test_get_request_household_code_confirm_address_data_no_cy(
            self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_address_cy,
                    data=self.common_postcode_input_valid)
            self.assertEqual(response.status, 200)

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_select_address_cy,
                    data=self.common_select_address_input_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_confirm:
                response = await self.client.request(
                    'POST',
                    self.post_request_household_code_confirm_address_cy,
                    data=self.common_confirm_address_input_no)
            self.assertLogEvent(cm_confirm, "received POST on endpoint 'cy/requests/household-code/confirm-address'")
            self.assertLogEvent(cm_confirm, "received GET on endpoint 'cy/requests/household-code/enter-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn(self.content_request_enter_address_title_cy, str(resp_content))
            self.assertIn(self.content_request_enter_address_secondary_cy, str(resp_content))

    @unittest_run_loop
    async def test_get_request_household_code_confirm_address_data_no_ni(
            self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_address_ni,
                    data=self.common_postcode_input_valid)
            self.assertEqual(response.status, 200)

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_select_address_ni,
                    data=self.common_select_address_input_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_confirm:
                response = await self.client.request(
                    'POST',
                    self.post_request_household_code_confirm_address_ni,
                    data=self.common_confirm_address_input_no)
            self.assertLogEvent(cm_confirm, "received POST on endpoint 'ni/requests/household-code/confirm-address'")
            self.assertLogEvent(cm_confirm, "received GET on endpoint 'ni/requests/household-code/enter-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_request_enter_address_title_en, str(resp_content))
            self.assertIn(self.content_request_enter_address_secondary_en, str(resp_content))

    @unittest_run_loop
    async def test_get_request_household_code_confirm_address_data_invalid_en(
            self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertEqual(response.status, 200)

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_select_address_en,
                    data=self.common_select_address_input_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_confirm:
                response = await self.client.request(
                    'POST',
                    self.post_request_household_code_confirm_address_en,
                    data=self.common_confirm_address_input_invalid)
            self.assertLogEvent(cm_confirm, "received POST on endpoint 'en/requests/household-code/confirm-address'")
            self.assertLogEvent(cm_confirm, "address confirmation error")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_title_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_error_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_yes_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_change_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_no_en, str(resp_content))

    @unittest_run_loop
    async def test_get_request_household_code_confirm_address_data_invalid_cy(
            self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_address_cy,
                    data=self.common_postcode_input_valid)
            self.assertEqual(response.status, 200)

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_select_address_cy,
                    data=self.common_select_address_input_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_confirm:
                response = await self.client.request(
                    'POST',
                    self.post_request_household_code_confirm_address_cy,
                    data=self.common_confirm_address_input_invalid)
            self.assertLogEvent(cm_confirm, "received POST on endpoint 'cy/requests/household-code/confirm-address'")
            self.assertLogEvent(cm_confirm, "address confirmation error")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn(self.content_common_confirm_address_title_cy, str(resp_content))
            self.assertIn(self.content_common_confirm_address_error_cy, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_yes_cy, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_change_cy, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_no_cy, str(resp_content))

    @unittest_run_loop
    async def test_get_request_household_code_confirm_address_data_invalid_ni(
            self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_address_ni,
                    data=self.common_postcode_input_valid)
            self.assertEqual(response.status, 200)

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_select_address_ni,
                    data=self.common_select_address_input_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_confirm:
                response = await self.client.request(
                    'POST',
                    self.post_request_household_code_confirm_address_ni,
                    data=self.common_confirm_address_input_invalid)
            self.assertLogEvent(cm_confirm, "received POST on endpoint 'ni/requests/household-code/confirm-address'")
            self.assertLogEvent(cm_confirm, "address confirmation error")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_common_confirm_address_title_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_error_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_yes_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_change_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_no_en, str(resp_content))

    @unittest_run_loop
    async def test_get_request_household_code_confirm_address_no_selection_en(
            self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertEqual(response.status, 200)

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_select_address_en,
                    data=self.common_select_address_input_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_confirm:
                response = await self.client.request(
                    'POST',
                    self.post_request_household_code_confirm_address_en,
                    data=self.common_form_data_empty)
            self.assertLogEvent(cm_confirm, "received POST on endpoint 'en/requests/household-code/confirm-address'")
            self.assertLogEvent(cm_confirm, "address confirmation error")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_title_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_error_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_yes_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_change_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_no_en, str(resp_content))

    @unittest_run_loop
    async def test_get_request_household_code_confirm_address_no_selection_cy(
            self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_address_cy,
                    data=self.common_postcode_input_valid)
            self.assertEqual(response.status, 200)

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_select_address_cy,
                    data=self.common_select_address_input_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_confirm:
                response = await self.client.request(
                    'POST',
                    self.post_request_household_code_confirm_address_cy,
                    data=self.common_form_data_empty)
            self.assertLogEvent(cm_confirm, "received POST on endpoint 'cy/requests/household-code/confirm-address'")
            self.assertLogEvent(cm_confirm, "address confirmation error")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn(self.content_common_confirm_address_title_cy, str(resp_content))
            self.assertIn(self.content_common_confirm_address_error_cy, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_yes_cy, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_change_cy, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_no_cy, str(resp_content))

    @unittest_run_loop
    async def test_get_request_household_code_confirm_address_no_selection_ni(
            self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_address_ni,
                    data=self.common_postcode_input_valid)
            self.assertEqual(response.status, 200)

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_select_address_ni,
                    data=self.common_select_address_input_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_confirm:
                response = await self.client.request(
                    'POST',
                    self.post_request_household_code_confirm_address_ni,
                    data=self.common_form_data_empty)
            self.assertLogEvent(cm_confirm, "received POST on endpoint 'ni/requests/household-code/confirm-address'")
            self.assertLogEvent(cm_confirm, "address confirmation error")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_common_confirm_address_title_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_error_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_yes_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_change_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_no_en, str(resp_content))

    @unittest_run_loop
    async def test_post_request_household_code_select_address_no_selection_en(
            self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_select:
                response = await self.client.request(
                    'POST',
                    self.post_request_household_code_select_address_en,
                    data=self.common_form_data_empty)
            self.assertLogEvent(cm_select, "received POST on endpoint 'en/requests/household-code/select-address'")
            self.assertLogEvent(cm_select, "no address selected")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn(self.content_common_select_address_title_en, str(resp_content))
            self.assertIn(self.content_common_select_address_error_en, str(resp_content))
            self.assertIn(self.content_common_select_address_value_en, str(resp_content))

    @unittest_run_loop
    async def test_post_request_household_code_select_address_no_selection_cy(
            self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_address_cy,
                    data=self.common_postcode_input_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_select:
                response = await self.client.request(
                    'POST',
                    self.post_request_household_code_select_address_cy,
                    data=self.common_form_data_empty)
            self.assertLogEvent(cm_select, "received POST on endpoint 'cy/requests/household-code/select-address'")
            self.assertLogEvent(cm_select, "no address selected")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn(self.content_common_select_address_title_cy, str(resp_content))
            self.assertIn(self.content_common_select_address_error_cy, str(resp_content))
            self.assertIn(self.content_common_select_address_value_cy, str(resp_content))

    @unittest_run_loop
    async def test_post_request_household_code_select_address_no_selection_ni(
            self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            response = await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_address_ni,
                    data=self.common_postcode_input_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_select:
                response = await self.client.request(
                    'POST',
                    self.post_request_household_code_select_address_ni,
                    data=self.common_form_data_empty)
            self.assertLogEvent(cm_select, "received POST on endpoint 'ni/requests/household-code/select-address'")
            self.assertLogEvent(cm_select, "no address selected")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_common_select_address_title_en, str(resp_content))
            self.assertIn(self.content_common_select_address_error_en, str(resp_content))
            self.assertIn(self.content_common_select_address_value_en, str(resp_content))

    @unittest_run_loop
    async def test_post_request_household_code_get_ai_postcode_500_en(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       status=500)

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'error in response', status_code=500)

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_post_request_household_code_get_ai_postcode_500_cy(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       status=500)

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_address_cy,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'error in response', status_code=500)

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_cy, contents)
        self.assertIn(self.content_common_500_error_cy, contents)

    @unittest_run_loop
    async def test_post_request_household_code_get_ai_postcode_500_ni(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       status=500)

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_address_ni,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'error in response', status_code=500)

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.nisra_logo, contents)
        self.assertIn(self.content_common_500_error_en, contents)

    def mock503s(self, mocked, times):
        for i in range(times):
            mocked.get(self.addressindexsvc_url + self.postcode_valid, status=503)

    @unittest_run_loop
    async def test_post_request_household_code_get_ai_postcode_503_en(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            self.mock503s(mocked, attempts_retry_limit)

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'error in response', status_code=503)

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_post_request_household_code_get_ai_postcode_503_cy(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            self.mock503s(mocked, attempts_retry_limit)

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_address_cy,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'error in response', status_code=503)

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_cy, contents)
        self.assertIn(self.content_common_500_error_cy, contents)

    @unittest_run_loop
    async def test_post_request_household_code_get_ai_postcode_503_ni(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            self.mock503s(mocked, attempts_retry_limit)

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_address_ni,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'error in response', status_code=503)

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.nisra_logo, contents)
        self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_post_request_household_code_get_ai_postcode_403_en(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       status=403)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'error in response', status_code=403)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_post_request_household_code_get_ai_postcode_403_cy(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       status=403)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_address_cy,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'error in response', status_code=403)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn(self.content_common_500_error_cy,
                          contents)

    @unittest_run_loop
    async def test_post_request_household_code_get_ai_postcode_403_ni(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       status=403)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_address_ni,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'error in response', status_code=403)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_post_request_household_code_get_ai_postcode_401_en(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       status=401)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'error in response', status_code=401)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_post_request_household_code_get_ai_postcode_401_cy(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       status=401)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_address_cy,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'error in response', status_code=401)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn(self.content_common_500_error_cy,
                          contents)

    @unittest_run_loop
    async def test_post_request_household_code_get_ai_postcode_401_ni(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       status=401)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_address_ni,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'error in response', status_code=401)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_post_request_household_code_get_ai_postcode_400_en(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       status=400)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_post_request_household_code_get_ai_postcode_400_cy(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       status=400)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_address_cy,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn(self.content_common_500_error_cy,
                          contents)

    @unittest_run_loop
    async def test_post_request_household_code_get_ai_postcode_400_ni(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       status=400)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_request_household_code_enter_address_ni,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_common_500_error_en, contents)


# noinspection PyTypeChecker
class TestRequestsHandlersIndividualCode(RHTestCase):

    @unittest_run_loop
    async def test_request_individual_code_sms_happy_path_hh_en(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment'
        ) as mocked_request_fulfilment:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_hh_e
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi
            mocked_request_fulfilment.return_value = self.rhsvc_request_fulfilment

            response = await self.client.request('GET',
                                                 self.get_request_individual_code_en)
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/individual-code'")
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_request_individual_title_en, contents)
            self.assertIn(self.content_request_secondary_en, contents)

            response = await self.client.request('GET',
                                                 self.get_request_individual_code_enter_address_en)
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/individual-code/enter-address'")
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_request_enter_address_title_en, contents)
            self.assertIn(self.content_request_enter_address_secondary_en, contents)

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'valid postcode')

            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/individual-code/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/individual-code/select-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn(self.content_common_select_address_title_en, str(resp_content))
            self.assertIn(self.content_common_select_address_value_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_select_address_en,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/individual-code/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/individual-code/confirm-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_title_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_yes_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_change_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_no_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/individual-code/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/individual-code/enter-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_title_en, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_secondary_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_mobile_en,
                    data=self.request_code_enter_mobile_form_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/individual-code/enter-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/individual-code/confirm-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_title_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_confirm_mobile_en,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/individual-code/confirm-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/individual-code/code-sent'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn(self.content_request_code_sent_title_en, str(resp_content))

    @unittest_run_loop
    async def test_request_individual_code_sms_happy_path_hh_cy(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment'
        ) as mocked_request_fulfilment:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_hh_w
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi
            mocked_request_fulfilment.return_value = self.rhsvc_request_fulfilment

            response = await self.client.request('GET',
                                                 self.get_request_individual_code_cy)
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/individual-code'")
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn(self.content_request_individual_title_cy, contents)
            self.assertIn(self.content_request_secondary_cy, contents)

            response = await self.client.request('GET',
                                                 self.get_request_individual_code_enter_address_cy)
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/individual-code/enter-address'")
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn(self.content_request_enter_address_title_cy, contents)
            self.assertIn(self.content_request_enter_address_secondary_cy, contents)

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_address_cy,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'valid postcode')

            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/individual-code/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/individual-code/select-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn(self.content_common_select_address_title_cy, str(resp_content))
            self.assertIn(self.content_common_select_address_value_cy, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_select_address_cy,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/individual-code/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/individual-code/confirm-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn(self.content_common_confirm_address_title_cy, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_yes_cy, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_change_cy, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_no_cy, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_confirm_address_cy,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/individual-code/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/individual-code/enter-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_title_cy, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_secondary_cy, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_mobile_cy,
                    data=self.request_code_enter_mobile_form_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/individual-code/enter-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/individual-code/confirm-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_title_cy, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_confirm_mobile_cy,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/individual-code/confirm-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/individual-code/code-sent'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn(self.content_request_code_sent_title_cy, str(resp_content))

    @unittest_run_loop
    async def test_request_individual_code_sms_happy_path_hh_ni(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn, mock.patch(
            'app.utils.RHService.get_fulfilment'
        ) as mocked_get_fulfilment, mock.patch(
            'app.utils.RHService.request_fulfilment'
        ) as mocked_request_fulfilment:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_hh_n
            mocked_get_fulfilment.return_value = self.rhsvc_get_fulfilment_multi
            mocked_request_fulfilment.return_value = self.rhsvc_request_fulfilment

            response = await self.client.request('GET',
                                                 self.get_request_individual_code_ni)
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/individual-code'")
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_request_individual_title_en, contents)
            self.assertIn(self.content_request_secondary_en, contents)

            response = await self.client.request('GET',
                                                 self.get_request_individual_code_enter_address_ni)
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/individual-code/enter-address'")
            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_request_enter_address_title_en, contents)
            self.assertIn(self.content_request_enter_address_secondary_en, contents)

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_address_ni,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'valid postcode')

            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/individual-code/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/individual-code/select-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_common_select_address_title_en, str(resp_content))
            self.assertIn(self.content_common_select_address_value_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_select_address_ni,
                    data=self.common_select_address_input_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/individual-code/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/individual-code/confirm-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_common_confirm_address_title_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_yes_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_change_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_no_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_confirm_address_ni,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/individual-code/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/individual-code/enter-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_title_en, str(resp_content))
            self.assertIn(self.content_request_enter_mobile_secondary_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_mobile_ni,
                    data=self.request_code_enter_mobile_form_data_valid)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/individual-code/enter-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/individual-code/confirm-mobile'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_request_confirm_mobile_title_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_confirm_mobile_ni,
                    data=self.request_code_mobile_confirmation_data_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/individual-code/confirm-mobile'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/individual-code/code-sent'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_request_code_sent_title_en, str(resp_content))

    @unittest_run_loop
    async def test_post_request_individual_code_enter_address_not_found_en(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, \
                mock.patch('app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode:

            mocked_get_ai_postcode.return_value = self.ai_postcode_no_results

            response = await self.client.request(
                'POST',
                self.post_request_individual_code_enter_address_en,
                data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'valid postcode')

            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/individual-code/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/individual-code/select-address'")

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_common_select_address_no_results_en, contents)

    @unittest_run_loop
    async def test_post_request_individual_code_enter_address_not_found_cy(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, \
                mock.patch('app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode:

            mocked_get_ai_postcode.return_value = self.ai_postcode_no_results

            response = await self.client.request(
                'POST',
                self.post_request_individual_code_enter_address_cy,
                data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'valid postcode')

            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/individual-code/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/individual-code/select-address'")

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn(self.content_common_select_address_no_results_cy, contents)

    @unittest_run_loop
    async def test_post_request_individual_code_enter_address_not_found_ni(
            self):
        with self.assertLogs('respondent-home', 'INFO') as cm, \
                mock.patch('app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode:

            mocked_get_ai_postcode.return_value = self.ai_postcode_no_results

            response = await self.client.request(
                'POST',
                self.post_request_individual_code_enter_address_ni,
                data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'valid postcode')

            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/individual-code/enter-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/individual-code/select-address'")

            self.assertEqual(response.status, 200)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_common_select_address_no_results_en, contents)

    @unittest_run_loop
    async def test_post_request_individual_code_get_ai_postcode_connection_error_en(
            self):
        with self.assertLogs('respondent-home', 'WARN') as cm, \
                aioresponses(passthrough=[str(self.server._root)]) as mocked:

            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       exception=ClientConnectionError('Failed'))

            response = await self.client.request(
                'POST',
                self.post_request_individual_code_enter_address_en,
                data=self.common_postcode_input_valid)

            self.assertLogEvent(cm,
                                'client failed to connect',
                                url=self.addressindexsvc_url +
                                self.postcode_valid +
                                self.address_index_epoch_param)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_post_request_individual_code_get_ai_postcode_connection_error_cy(
            self):
        with self.assertLogs('respondent-home', 'WARN') as cm, \
                aioresponses(passthrough=[str(self.server._root)]) as mocked:

            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       exception=ClientConnectionError('Failed'))

            response = await self.client.request(
                'POST',
                self.post_request_individual_code_enter_address_cy,
                data=self.common_postcode_input_valid)

            self.assertLogEvent(cm,
                                'client failed to connect',
                                url=self.addressindexsvc_url +
                                self.postcode_valid +
                                self.address_index_epoch_param)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn(self.content_common_500_error_cy, contents)

    @unittest_run_loop
    async def test_post_request_individual_code_get_ai_postcode_connection_error_ni(
            self):
        with self.assertLogs('respondent-home', 'WARN') as cm, \
                aioresponses(passthrough=[str(self.server._root)]) as mocked:

            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       exception=ClientConnectionError('Failed'))

            response = await self.client.request(
                'POST',
                self.post_request_individual_code_enter_address_ni,
                data=self.common_postcode_input_valid)

            self.assertLogEvent(cm,
                                'client failed to connect',
                                url=self.addressindexsvc_url +
                                self.postcode_valid +
                                self.address_index_epoch_param)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_post_request_individual_code_get_ai_postcode_connection_error_with_epoch_en(
            self):
        with self.assertLogs('respondent-home', 'WARN') as cm, \
                aioresponses(passthrough=[str(self.server._root)]) as mocked:

            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       exception=ClientConnectionError('Failed'))
            self.app['ADDRESS_INDEX_EPOCH'] = 'test'

            response = await self.client.request(
                'POST',
                self.post_request_individual_code_enter_address_en,
                data=self.common_postcode_input_valid)

            self.assertLogEvent(cm,
                                'client failed to connect',
                                url=self.addressindexsvc_url +
                                self.postcode_valid +
                                self.address_index_epoch_param_test)

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_post_request_individual_code_get_ai_postcode_connection_error_with_epoch_cy(
            self):
        with self.assertLogs('respondent-home', 'WARN') as cm, \
                aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       exception=ClientConnectionError('Failed'))
            self.app['ADDRESS_INDEX_EPOCH'] = 'test'

            response = await self.client.request(
                'POST',
                self.post_request_individual_code_enter_address_cy,
                data=self.common_postcode_input_valid)

            self.assertLogEvent(cm,
                                'client failed to connect',
                                url=self.addressindexsvc_url +
                                self.postcode_valid +
                                self.address_index_epoch_param_test)

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_cy, contents)
        self.assertIn(self.content_common_500_error_cy, contents)

    @unittest_run_loop
    async def test_post_request_individual_code_get_ai_postcode_connection_error_with_epoch_ni(
            self):
        with self.assertLogs('respondent-home', 'WARN') as cm, \
                aioresponses(passthrough=[str(self.server._root)]) as mocked:

            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       exception=ClientConnectionError('Failed'))
            self.app['ADDRESS_INDEX_EPOCH'] = 'test'

            response = await self.client.request(
                'POST',
                self.post_request_individual_code_enter_address_ni,
                data=self.common_postcode_input_valid)

            self.assertLogEvent(cm,
                                'client failed to connect',
                                url=self.addressindexsvc_url +
                                self.postcode_valid +
                                self.address_index_epoch_param_test)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_get_request_individual_code_address_in_scotland_en(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, mock.patch(
            'app.utils.RHService.get_case_by_uprn'
        ) as mocked_get_case_by_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result_scotland
            mocked_get_case_by_uprn.return_value = self.rhsvc_case_by_uprn_hh_e

            await self.client.request('GET', self.get_request_individual_code_en)
            await self.client.request('GET', self.get_request_individual_code_enter_address_en)
            await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_address_en,
                    data=self.common_postcode_input_valid)

            response_get_confirm = await self.client.request(
                    'POST',
                    self.post_request_individual_code_select_address_en,
                    data=self.common_select_address_input_valid)
            resp_content = await response_get_confirm.content.read()
            self.assertIn(self.content_common_confirm_address_value_yes_en, str(resp_content))
            self.assertNotIn(self.content_common_confirm_address_value_change_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_no_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/individual-code/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/address-in-scotland'")
            self.assertEqual(response.status, 200)

            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_common_address_in_scotland_en, contents)

    @unittest_run_loop
    async def test_get_request_individual_code_address_in_scotland_cy(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result_scotland

            await self.client.request('GET', self.get_request_individual_code_cy)
            await self.client.request('GET', self.get_request_individual_code_enter_address_cy)
            await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_address_cy,
                    data=self.common_postcode_input_valid)

            response_get_confirm = await self.client.request(
                    'POST',
                    self.post_request_individual_code_select_address_cy,
                    data=self.common_select_address_input_valid)
            resp_content = await response_get_confirm.content.read()
            self.assertIn(self.content_common_confirm_address_value_yes_cy, str(resp_content))
            self.assertNotIn(self.content_common_confirm_address_value_change_cy, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_no_cy, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_confirm_address_cy,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/individual-code/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/address-in-scotland'")
            self.assertEqual(response.status, 200)

            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn(self.content_common_address_in_scotland_cy, contents)

    @unittest_run_loop
    async def test_get_request_individual_code_address_in_scotland_ni(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result_scotland

            await self.client.request('GET', self.get_request_individual_code_ni)
            await self.client.request('GET', self.get_request_individual_code_enter_address_ni)
            await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_address_ni,
                    data=self.common_postcode_input_valid)

            response_get_confirm = await self.client.request(
                    'POST',
                    self.post_request_individual_code_select_address_ni,
                    data=self.common_select_address_input_valid)
            resp_content = await response_get_confirm.content.read()
            self.assertIn(self.content_common_confirm_address_value_yes_en, str(resp_content))
            self.assertNotIn(self.content_common_confirm_address_value_change_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_no_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_confirm_address_ni,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/individual-code/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/address-in-scotland'")
            self.assertEqual(response.status, 200)

            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_common_address_in_scotland_en, contents)

    @unittest_run_loop
    async def test_get_request_individual_code_address_not_found_en(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            await self.client.request('GET', self.get_request_individual_code_en)
            await self.client.request('GET', self.get_request_individual_code_enter_address_en)
            await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_address_en,
                    data=self.common_postcode_input_valid)
            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_select_address_en,
                    data=self.common_select_address_input_not_listed_en)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/individual-code/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/call-contact-centre/address-not-found'")
            self.assertEqual(response.status, 200)

            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_common_call_contact_centre_address_not_found_title_en, contents)

    @unittest_run_loop
    async def test_get_request_individual_code_address_not_found_cy(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            await self.client.request('GET', self.get_request_individual_code_cy)
            await self.client.request('GET', self.get_request_individual_code_enter_address_cy)
            await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_address_cy,
                    data=self.common_postcode_input_valid)
            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_select_address_cy,
                    data=self.common_select_address_input_not_listed_cy)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/individual-code/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/call-contact-centre/address-not-found'")
            self.assertEqual(response.status, 200)

            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn(self.content_common_call_contact_centre_address_not_found_title_cy, contents)

    @unittest_run_loop
    async def test_get_request_individual_code_address_not_found_ni(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            await self.client.request('GET', self.get_request_individual_code_ni)
            await self.client.request('GET', self.get_request_individual_code_enter_address_ni)
            await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_address_ni,
                    data=self.common_postcode_input_valid)
            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_select_address_ni,
                    data=self.common_select_address_input_not_listed_en)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/individual-code/select-address'")
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/call-contact-centre/address-not-found'")
            self.assertEqual(response.status, 200)

            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_common_call_contact_centre_address_not_found_title_en, contents)

    @unittest_run_loop
    async def test_get_request_individual_code_census_address_type_na_en(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result_censusaddresstype_na

            await self.client.request('GET', self.get_request_individual_code_en)
            await self.client.request('GET', self.get_request_individual_code_enter_address_en)
            await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_address_en,
                    data=self.common_postcode_input_valid)

            response_get_confirm = await self.client.request(
                    'POST',
                    self.post_request_individual_code_select_address_en,
                    data=self.common_select_address_input_valid)
            resp_content = await response_get_confirm.content.read()
            self.assertIn(self.content_common_confirm_address_value_yes_en, str(resp_content))
            self.assertNotIn(self.content_common_confirm_address_value_change_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_no_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/individual-code/confirm-address'")
            self.assertLogEvent(cm,
                                "received GET on endpoint 'en/requests/call-contact-centre/unable-to-match-address'")

            self.assertEqual(200, response.status)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn(self.content_common_call_contact_centre_title_en, str(resp_content))
            self.assertIn(self.content_common_call_contact_centre_unable_to_match_address_en, str(resp_content))

    @unittest_run_loop
    async def test_get_request_individual_code_census_address_type_na_cy(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result_censusaddresstype_na

            await self.client.request('GET', self.get_request_individual_code_cy)
            await self.client.request('GET', self.get_request_individual_code_enter_address_cy)
            await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_address_cy,
                    data=self.common_postcode_input_valid)

            response_get_confirm = await self.client.request(
                    'POST',
                    self.post_request_individual_code_select_address_cy,
                    data=self.common_select_address_input_valid)
            resp_content = await response_get_confirm.content.read()
            self.assertIn(self.content_common_confirm_address_value_yes_cy, str(resp_content))
            self.assertNotIn(self.content_common_confirm_address_value_change_cy, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_no_cy, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_confirm_address_cy,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/individual-code/confirm-address'")
            self.assertLogEvent(cm,
                                "received GET on endpoint 'cy/requests/call-contact-centre/unable-to-match-address'")

            self.assertEqual(200, response.status)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn(self.content_common_call_contact_centre_title_cy, str(resp_content))
            self.assertIn(self.content_common_call_contact_centre_unable_to_match_address_cy, str(resp_content))

    @unittest_run_loop
    async def test_get_request_individual_code_census_address_type_na_ni(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result_censusaddresstype_na

            await self.client.request('GET', self.get_request_individual_code_ni)
            await self.client.request('GET', self.get_request_individual_code_enter_address_ni)
            await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_address_ni,
                    data=self.common_postcode_input_valid)

            response_get_confirm = await self.client.request(
                    'POST',
                    self.post_request_individual_code_select_address_ni,
                    data=self.common_select_address_input_valid)
            resp_content = await response_get_confirm.content.read()
            self.assertIn(self.content_common_confirm_address_value_yes_en, str(resp_content))
            self.assertNotIn(self.content_common_confirm_address_value_change_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_no_en, str(resp_content))

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_confirm_address_ni,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/individual-code/confirm-address'")
            self.assertLogEvent(cm,
                                "received GET on endpoint 'ni/requests/call-contact-centre/unable-to-match-address'")

            self.assertEqual(200, response.status)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_common_call_contact_centre_title_en, str(resp_content))
            self.assertIn(self.content_common_call_contact_centre_unable_to_match_address_en, str(resp_content))

    @unittest_run_loop
    async def test_get_request_individual_code_confirm_address_data_change_en(
            self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertEqual(response.status, 200)

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_select_address_en,
                    data=self.common_select_address_input_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_confirm:
                response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_confirm_address_en,
                    data=self.common_confirm_address_input_change)
            self.assertLogEvent(cm_confirm, "received POST on endpoint 'en/requests/individual-code/confirm-address'")
            self.assertLogEvent(cm_confirm,
                                "received GET on endpoint 'en/requests/call-contact-centre/address-not-found'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn(self.content_common_call_contact_centre_address_not_found_title_en, str(resp_content))
            self.assertIn(self.content_common_call_contact_centre_address_not_found_text_en, str(resp_content))

    @unittest_run_loop
    async def test_get_request_individual_code_confirm_address_data_change_cy(
            self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_address_cy,
                    data=self.common_postcode_input_valid)
            self.assertEqual(response.status, 200)

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_select_address_cy,
                    data=self.common_select_address_input_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_confirm:
                response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_confirm_address_cy,
                    data=self.common_confirm_address_input_change)
            self.assertLogEvent(cm_confirm, "received POST on endpoint 'cy/requests/individual-code/confirm-address'")
            self.assertLogEvent(cm_confirm,
                                "received GET on endpoint 'cy/requests/call-contact-centre/address-not-found'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn(self.content_common_call_contact_centre_address_not_found_title_cy, str(resp_content))
            self.assertIn(self.content_common_call_contact_centre_address_not_found_text_cy, str(resp_content))

    @unittest_run_loop
    async def test_get_request_individual_code_confirm_address_data_change_ni(
            self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_address_ni,
                    data=self.common_postcode_input_valid)
            self.assertEqual(response.status, 200)

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_select_address_ni,
                    data=self.common_select_address_input_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_confirm:
                response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_confirm_address_ni,
                    data=self.common_confirm_address_input_change)
            self.assertLogEvent(cm_confirm, "received POST on endpoint 'ni/requests/individual-code/confirm-address'")
            self.assertLogEvent(cm_confirm,
                                "received GET on endpoint 'ni/requests/call-contact-centre/address-not-found'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_common_call_contact_centre_address_not_found_title_en, str(resp_content))
            self.assertIn(self.content_common_call_contact_centre_address_not_found_text_en, str(resp_content))

    @unittest_run_loop
    async def test_post_request_individual_code_enter_address_bad_postcode_en(
            self):

        with self.assertLogs('respondent-home', 'INFO') as cm:

            await self.client.request('GET', self.get_request_individual_code_en)

            await self.client.request('GET', self.get_request_individual_code_enter_address_en)
            self.assertLogEvent(cm, "received GET on endpoint 'en/requests/individual-code/enter-address'")

            response = await self.client.request(
                'POST',
                self.post_request_individual_code_enter_address_en,
                data=self.common_postcode_input_invalid)
        self.assertLogEvent(cm, 'invalid postcode')
        self.assertLogEvent(cm, "received POST on endpoint 'en/requests/individual-code/enter-address'")

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertIn(self.content_request_enter_address_title_en, contents)
        self.assertIn(self.content_common_enter_address_error_en, contents)
        self.assertIn(self.content_request_enter_address_secondary_en, contents)

    @unittest_run_loop
    async def test_post_request_individual_code_enter_address_bad_postcode_cy(
            self):

        with self.assertLogs('respondent-home', 'INFO') as cm:

            await self.client.request('GET', self.get_request_individual_code_cy)

            await self.client.request('GET', self.get_request_individual_code_enter_address_cy)
            self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/individual-code/enter-address'")

            response = await self.client.request(
                'POST',
                self.post_request_individual_code_enter_address_cy,
                data=self.common_postcode_input_invalid)
        self.assertLogEvent(cm, 'invalid postcode')
        self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/individual-code/enter-address'")

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_cy, contents)
        self.assertIn(self.content_request_enter_address_title_cy, contents)
        self.assertIn(self.content_common_enter_address_error_cy, contents)
        self.assertIn(self.content_request_enter_address_secondary_cy, contents)

    @unittest_run_loop
    async def test_post_request_individual_code_enter_address_bad_postcode_ni(
            self):

        with self.assertLogs('respondent-home', 'INFO') as cm:

            await self.client.request('GET', self.get_request_individual_code_ni)

            await self.client.request('GET', self.get_request_individual_code_enter_address_ni)
            self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/individual-code/enter-address'")

            response = await self.client.request(
                'POST',
                self.post_request_individual_code_enter_address_ni,
                data=self.common_postcode_input_invalid)
        self.assertLogEvent(cm, 'invalid postcode')
        self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/individual-code/enter-address'")

        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.nisra_logo, contents)
        self.assertIn(self.content_request_enter_address_title_en, contents)
        self.assertIn(self.content_common_enter_address_error_en, contents)
        self.assertIn(self.content_request_enter_address_secondary_en, contents)

    @unittest_run_loop
    async def test_get_request_individual_code_timeout_en(self):

        with self.assertLogs('respondent-home', 'INFO') as cm:

            response = await self.client.request('GET',
                                                 self.get_request_individual_code_timeout_en)
        self.assertLogEvent(cm, "received GET on endpoint 'en/requests/individual-code/timeout'")
        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertIn(self.content_common_timeout_en, contents)
        self.assertIn(self.content_request_timeout_error_en, contents)

    @unittest_run_loop
    async def test_get_request_individual_code_timeout_cy(self):

        with self.assertLogs('respondent-home', 'INFO') as cm:

            response = await self.client.request('GET',
                                                 self.get_request_individual_code_timeout_cy)
        self.assertLogEvent(cm, "received GET on endpoint 'cy/requests/individual-code/timeout'")
        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_cy, contents)
        self.assertIn(self.content_common_timeout_cy, contents)
        self.assertIn(self.content_request_timeout_error_cy, contents)

    @unittest_run_loop
    async def test_get_request_individual_code_timeout_ni(self):

        with self.assertLogs('respondent-home', 'INFO') as cm:

            response = await self.client.request('GET',
                                                 self.get_request_individual_code_timeout_ni)
        self.assertLogEvent(cm, "received GET on endpoint 'ni/requests/individual-code/timeout'")
        self.assertEqual(response.status, 200)
        contents = str(await response.content.read())
        self.assertIn(self.nisra_logo, contents)
        self.assertIn(self.content_common_timeout_en, contents)
        self.assertIn(self.content_request_timeout_error_en, contents)

    @unittest_run_loop
    async def test_get_request_individual_code_confirm_address_get_cases_error_en(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode'
        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn'
        ) as mocked_get_ai_uprn, aioresponses(
            passthrough=[str(self.server._root)]
        ) as mocked_get_case_by_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.get(self.rhsvc_cases_by_uprn_url + self.selected_uprn, status=400)

            await self.client.request('GET', self.get_request_individual_code_en)
            await self.client.request('GET', self.get_request_individual_code_enter_address_en)
            await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_address_en,
                    data=self.common_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_individual_code_select_address_en,
                    data=self.common_select_address_input_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/individual-code/confirm-address'")

            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_get_request_individual_code_confirm_address_get_cases_error_cy(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, aioresponses(
            passthrough=[str(self.server._root)]
        ) as mocked_get_case_by_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.get(self.rhsvc_cases_by_uprn_url + self.selected_uprn, status=400)

            await self.client.request('GET', self.get_request_individual_code_cy)
            await self.client.request('GET', self.get_request_individual_code_enter_address_cy)
            await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_address_cy,
                    data=self.common_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_individual_code_select_address_cy,
                    data=self.common_select_address_input_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_confirm_address_cy,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/individual-code/confirm-address'")

            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn(self.content_common_500_error_cy, contents)

    @unittest_run_loop
    async def test_get_request_individual_code_confirm_address_get_cases_error_ni(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, aioresponses(
            passthrough=[str(self.server._root)]
        ) as mocked_get_case_by_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.get(self.rhsvc_cases_by_uprn_url + self.selected_uprn, status=400)

            await self.client.request('GET', self.get_request_individual_code_ni)
            await self.client.request('GET', self.get_request_individual_code_enter_address_ni)
            await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_address_ni,
                    data=self.common_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_individual_code_select_address_ni,
                    data=self.common_select_address_input_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_confirm_address_ni,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/individual-code/confirm-address'")

            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_get_request_individual_address_not_required_en(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, aioresponses(
            passthrough=[str(self.server._root)]
        ) as mocked_get_case_by_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.get(self.rhsvc_cases_by_uprn_url + self.selected_uprn, status=404)

            await self.client.request('GET', self.get_request_individual_code_en)
            await self.client.request('GET', self.get_request_individual_code_enter_address_en)
            await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_address_en,
                    data=self.common_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_individual_code_select_address_en,
                    data=self.common_select_address_input_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_confirm_address_en,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'en/requests/individual-code/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint "
                                    "'en/requests/call-contact-centre/unable-to-match-address'")

            self.assertEqual(response.status, 200)

            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_request_contact_centre_en, contents)

    @unittest_run_loop
    async def test_get_request_individual_address_not_required_cy(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, aioresponses(
            passthrough=[str(self.server._root)]
        ) as mocked_get_case_by_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.get(self.rhsvc_cases_by_uprn_url + self.selected_uprn, status=404)

            await self.client.request('GET', self.get_request_individual_code_cy)
            await self.client.request('GET', self.get_request_individual_code_enter_address_cy)
            await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_address_cy,
                    data=self.common_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_individual_code_select_address_cy,
                    data=self.common_select_address_input_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_confirm_address_cy,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'cy/requests/individual-code/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint "
                                    "'cy/requests/call-contact-centre/unable-to-match-address'")

            self.assertEqual(response.status, 200)

            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn(self.content_request_contact_centre_cy, contents)

    @unittest_run_loop
    async def test_get_request_individual_address_not_required_ni(self):
        with self.assertLogs('respondent-home', 'INFO') as cm, mock.patch(
                'app.utils.AddressIndex.get_ai_postcode') as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn, aioresponses(
            passthrough=[str(self.server._root)]
        ) as mocked_get_case_by_uprn:

            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result
            mocked_get_case_by_uprn.get(self.rhsvc_cases_by_uprn_url + self.selected_uprn, status=404)

            await self.client.request('GET', self.get_request_individual_code_ni)
            await self.client.request('GET', self.get_request_individual_code_enter_address_ni)
            await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_address_ni,
                    data=self.common_postcode_input_valid)
            await self.client.request(
                    'POST',
                    self.post_request_individual_code_select_address_ni,
                    data=self.common_select_address_input_valid)

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_confirm_address_ni,
                    data=self.common_confirm_address_input_yes)
            self.assertLogEvent(cm, "received POST on endpoint 'ni/requests/individual-code/confirm-address'")
            self.assertLogEvent(cm, "received GET on endpoint "
                                    "'ni/requests/call-contact-centre/unable-to-match-address'")

            self.assertEqual(response.status, 200)

            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_request_contact_centre_en, contents)

    @unittest_run_loop
    async def test_get_request_individual_code_confirm_address_data_no_en(
            self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertEqual(response.status, 200)

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_select_address_en,
                    data=self.common_select_address_input_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_confirm:
                response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_confirm_address_en,
                    data=self.common_confirm_address_input_no)
            self.assertLogEvent(cm_confirm, "received POST on endpoint 'en/requests/individual-code/confirm-address'")
            self.assertLogEvent(cm_confirm, "received GET on endpoint 'en/requests/individual-code/enter-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn(self.content_request_enter_address_title_en, str(resp_content))
            self.assertIn(self.content_request_enter_address_secondary_en, str(resp_content))

    @unittest_run_loop
    async def test_get_request_individual_confirm_address_data_no_cy(
            self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_address_cy,
                    data=self.common_postcode_input_valid)
            self.assertEqual(response.status, 200)

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_select_address_cy,
                    data=self.common_select_address_input_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_confirm:
                response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_confirm_address_cy,
                    data=self.common_confirm_address_input_no)
            self.assertLogEvent(cm_confirm, "received POST on endpoint 'cy/requests/individual-code/confirm-address'")
            self.assertLogEvent(cm_confirm, "received GET on endpoint 'cy/requests/individual-code/enter-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn(self.content_request_enter_address_title_cy, str(resp_content))
            self.assertIn(self.content_request_enter_address_secondary_cy, str(resp_content))

    @unittest_run_loop
    async def test_get_request_individual_code_confirm_address_data_no_ni(
            self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_address_ni,
                    data=self.common_postcode_input_valid)
            self.assertEqual(response.status, 200)

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_select_address_ni,
                    data=self.common_select_address_input_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_confirm:
                response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_confirm_address_ni,
                    data=self.common_confirm_address_input_no)
            self.assertLogEvent(cm_confirm, "received POST on endpoint 'ni/requests/individual-code/confirm-address'")
            self.assertLogEvent(cm_confirm, "received GET on endpoint 'ni/requests/individual-code/enter-address'")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_request_enter_address_title_en, str(resp_content))
            self.assertIn(self.content_request_enter_address_secondary_en, str(resp_content))

    @unittest_run_loop
    async def test_get_request_individual_code_confirm_address_data_invalid_en(
            self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertEqual(response.status, 200)

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_select_address_en,
                    data=self.common_select_address_input_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_confirm:
                response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_confirm_address_en,
                    data=self.common_confirm_address_input_invalid)
            self.assertLogEvent(cm_confirm, "received POST on endpoint 'en/requests/individual-code/confirm-address'")
            self.assertLogEvent(cm_confirm, "address confirmation error")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_title_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_error_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_yes_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_change_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_no_en, str(resp_content))

    @unittest_run_loop
    async def test_get_request_individual_code_confirm_address_data_invalid_cy(
            self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_address_cy,
                    data=self.common_postcode_input_valid)
            self.assertEqual(response.status, 200)

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_select_address_cy,
                    data=self.common_select_address_input_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_confirm:
                response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_confirm_address_cy,
                    data=self.common_confirm_address_input_invalid)
            self.assertLogEvent(cm_confirm, "received POST on endpoint 'cy/requests/individual-code/confirm-address'")
            self.assertLogEvent(cm_confirm, "address confirmation error")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn(self.content_common_confirm_address_title_cy, str(resp_content))
            self.assertIn(self.content_common_confirm_address_error_cy, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_yes_cy, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_change_cy, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_no_cy, str(resp_content))

    @unittest_run_loop
    async def test_get_request_individual_code_confirm_address_data_invalid_ni(
            self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_address_ni,
                    data=self.common_postcode_input_valid)
            self.assertEqual(response.status, 200)

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_select_address_ni,
                    data=self.common_select_address_input_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_confirm:
                response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_confirm_address_ni,
                    data=self.common_confirm_address_input_invalid)
            self.assertLogEvent(cm_confirm, "received POST on endpoint 'ni/requests/individual-code/confirm-address'")
            self.assertLogEvent(cm_confirm, "address confirmation error")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_common_confirm_address_title_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_error_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_yes_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_change_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_no_en, str(resp_content))

    @unittest_run_loop
    async def test_get_request_individual_code_confirm_address_no_selection_en(
            self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertEqual(response.status, 200)

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_select_address_en,
                    data=self.common_select_address_input_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_confirm:
                response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_confirm_address_en,
                    data=self.common_form_data_empty)
            self.assertLogEvent(cm_confirm, "received POST on endpoint 'en/requests/individual-code/confirm-address'")
            self.assertLogEvent(cm_confirm, "address confirmation error")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_title_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_error_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_yes_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_change_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_no_en, str(resp_content))

    @unittest_run_loop
    async def test_get_request_individual_code_confirm_address_no_selection_cy(
            self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_address_cy,
                    data=self.common_postcode_input_valid)
            self.assertEqual(response.status, 200)

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_select_address_cy,
                    data=self.common_select_address_input_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_confirm:
                response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_confirm_address_cy,
                    data=self.common_form_data_empty)
            self.assertLogEvent(cm_confirm, "received POST on endpoint 'cy/requests/individual-code/confirm-address'")
            self.assertLogEvent(cm_confirm, "address confirmation error")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn(self.content_common_confirm_address_title_cy, str(resp_content))
            self.assertIn(self.content_common_confirm_address_error_cy, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_yes_cy, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_change_cy, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_no_cy, str(resp_content))

    @unittest_run_loop
    async def test_get_request_individual_code_confirm_address_no_selection_ni(
            self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode, mock.patch(
                'app.utils.AddressIndex.get_ai_uprn') as mocked_get_ai_uprn:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results
            mocked_get_ai_uprn.return_value = self.ai_uprn_result

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_address_ni,
                    data=self.common_postcode_input_valid)
            self.assertEqual(response.status, 200)

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_select_address_ni,
                    data=self.common_select_address_input_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_confirm:
                response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_confirm_address_ni,
                    data=self.common_form_data_empty)
            self.assertLogEvent(cm_confirm, "received POST on endpoint 'ni/requests/individual-code/confirm-address'")
            self.assertLogEvent(cm_confirm, "address confirmation error")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_common_confirm_address_title_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_error_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_yes_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_change_en, str(resp_content))
            self.assertIn(self.content_common_confirm_address_value_no_en, str(resp_content))

    @unittest_run_loop
    async def test_post_request_individual_code_select_address_no_selection_en(
            self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_select:
                response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_select_address_en,
                    data=self.common_form_data_empty)
            self.assertLogEvent(cm_select, "received POST on endpoint 'en/requests/individual-code/select-address'")
            self.assertLogEvent(cm_select, "no address selected")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_en, str(resp_content))
            self.assertIn(self.content_common_select_address_title_en, str(resp_content))
            self.assertIn(self.content_common_select_address_error_en, str(resp_content))
            self.assertIn(self.content_common_select_address_value_en, str(resp_content))

    @unittest_run_loop
    async def test_post_request_individual_code_select_address_no_selection_cy(
            self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_address_cy,
                    data=self.common_postcode_input_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_select:
                response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_select_address_cy,
                    data=self.common_form_data_empty)
            self.assertLogEvent(cm_select, "received POST on endpoint 'cy/requests/individual-code/select-address'")
            self.assertLogEvent(cm_select, "no address selected")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.ons_logo_cy, str(resp_content))
            self.assertIn(self.content_common_select_address_title_cy, str(resp_content))
            self.assertIn(self.content_common_select_address_error_cy, str(resp_content))
            self.assertIn(self.content_common_select_address_value_cy, str(resp_content))

    @unittest_run_loop
    async def test_post_request_individual_code_select_address_no_selection_ni(
            self):
        with mock.patch('app.utils.AddressIndex.get_ai_postcode'
                        ) as mocked_get_ai_postcode:
            mocked_get_ai_postcode.return_value = self.ai_postcode_results

            response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_address_ni,
                    data=self.common_postcode_input_valid)
            self.assertEqual(response.status, 200)

            with self.assertLogs('respondent-home', 'INFO') as cm_select:
                response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_select_address_ni,
                    data=self.common_form_data_empty)
            self.assertLogEvent(cm_select, "received POST on endpoint 'ni/requests/individual-code/select-address'")
            self.assertLogEvent(cm_select, "no address selected")

            self.assertEqual(response.status, 200)
            resp_content = await response.content.read()
            self.assertIn(self.nisra_logo, str(resp_content))
            self.assertIn(self.content_common_select_address_title_en, str(resp_content))
            self.assertIn(self.content_common_select_address_error_en, str(resp_content))
            self.assertIn(self.content_common_select_address_value_en, str(resp_content))

    @unittest_run_loop
    async def test_post_request_individual_code_get_ai_postcode_500_en(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       status=500)

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'error in response', status_code=500)

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_post_request_individual_code_get_ai_postcode_500_cy(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       status=500)

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_address_cy,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'error in response', status_code=500)

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_cy, contents)
        self.assertIn(self.content_common_500_error_cy, contents)

    @unittest_run_loop
    async def test_post_request_individual_code_get_ai_postcode_500_ni(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       status=500)

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_address_ni,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'error in response', status_code=500)

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.nisra_logo, contents)
        self.assertIn(self.content_common_500_error_en, contents)

    def mock503s(self, mocked, times):
        for i in range(times):
            mocked.get(self.addressindexsvc_url + self.postcode_valid, status=503)

    @unittest_run_loop
    async def test_post_request_individual_code_get_ai_postcode_503_en(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            self.mock503s(mocked, attempts_retry_limit)

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'error in response', status_code=503)

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_en, contents)
        self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_post_request_individual_code_get_ai_postcode_503_cy(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            self.mock503s(mocked, attempts_retry_limit)

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_address_cy,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'error in response', status_code=503)

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.ons_logo_cy, contents)
        self.assertIn(self.content_common_500_error_cy, contents)

    @unittest_run_loop
    async def test_post_request_individual_code_get_ai_postcode_503_ni(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            self.mock503s(mocked, attempts_retry_limit)

            with self.assertLogs('respondent-home', 'ERROR') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_address_ni,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'error in response', status_code=503)

        self.assertEqual(response.status, 500)
        contents = str(await response.content.read())
        self.assertIn(self.nisra_logo, contents)
        self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_post_request_individual_code_get_ai_postcode_403_en(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       status=403)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'error in response', status_code=403)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_post_request_individual_code_get_ai_postcode_403_cy(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       status=403)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_address_cy,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'error in response', status_code=403)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn(self.content_common_500_error_cy,
                          contents)

    @unittest_run_loop
    async def test_post_request_individual_code_get_ai_postcode_403_ni(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       status=403)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_address_ni,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'error in response', status_code=403)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_post_request_individual_code_get_ai_postcode_401_en(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       status=401)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'error in response', status_code=401)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_post_request_individual_code_get_ai_postcode_401_cy(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       status=401)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_address_cy,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'error in response', status_code=401)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn(self.content_common_500_error_cy,
                          contents)

    @unittest_run_loop
    async def test_post_request_individual_code_get_ai_postcode_401_ni(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       status=401)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_address_ni,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'error in response', status_code=401)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_post_request_individual_code_get_ai_postcode_400_en(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       status=400)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_address_en,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_en, contents)
            self.assertIn(self.content_common_500_error_en, contents)

    @unittest_run_loop
    async def test_post_request_individual_code_get_ai_postcode_400_cy(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       status=400)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_address_cy,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.ons_logo_cy, contents)
            self.assertIn(self.content_common_500_error_cy,
                          contents)

    @unittest_run_loop
    async def test_post_request_individual_code_get_ai_postcode_400_ni(self):
        with aioresponses(passthrough=[str(self.server._root)]) as mocked:
            mocked.get(self.addressindexsvc_url + self.postcode_valid,
                       status=400)

            with self.assertLogs('respondent-home', 'INFO') as cm:
                response = await self.client.request(
                    'POST',
                    self.post_request_individual_code_enter_address_ni,
                    data=self.common_postcode_input_valid)
            self.assertLogEvent(cm, 'error in response', status_code=400)

            self.assertEqual(response.status, 500)
            contents = str(await response.content.read())
            self.assertIn(self.nisra_logo, contents)
            self.assertIn(self.content_common_500_error_en, contents)