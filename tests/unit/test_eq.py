from unittest import mock
from aiohttp.test_utils import unittest_run_loop
from app.eq import EqPayloadConstructor
from app.exceptions import InvalidEqPayLoad

from . import RHTestCase


class TestEq(RHTestCase):
    def test_create_eq_constructor(self):
        self.assertIsInstance(
            EqPayloadConstructor(self.uac_json_e, self.attributes_en, self.app), EqPayloadConstructor)

    def verify_missing(self, uac_json, expected_msg):
        with self.assertRaises(InvalidEqPayLoad) as ex:
            EqPayloadConstructor(uac_json, self.attributes_en, self.app)
        self.assertIn(expected_msg, ex.exception.message)

    def test_create_eq_constructor_missing_case_id(self):
        uac_json = self.uac_json_e.copy()
        del uac_json['collectionCase']['caseId']
        self.verify_missing(uac_json, 'No case id in supplied UAC context JSON')

    def test_create_eq_constructor_missing_ce_id(self):
        uac_json = self.uac_json_e.copy()
        del uac_json['collectionExercise']['collectionExerciseId']
        self.verify_missing(uac_json, 'No collection id in supplied UAC context JSON')

    def test_create_eq_constructor_missing_questionnaire_id(self):
        uac_json = self.uac_json_e.copy()
        del uac_json['qid']
        self.verify_missing(uac_json, 'No questionnaireId in supplied UAC context JSON')

    def test_create_eq_constructor_missing_uprn(self):
        uac_json = self.uac_json_e.copy()
        del uac_json['collectionCase']['sample']['uprn']
        self.verify_missing(uac_json, 'Could not retrieve address uprn from UAC context JSON')

    def test_create_eq_constructor_missing_region(self):
        uac_json = self.uac_json_e.copy()
        del uac_json['collectionCase']['sample']['region']
        self.verify_missing(uac_json, 'Could not retrieve region from UAC context JSON')

    def test_create_eq_constructor_missing_collection_name(self):
        uac_json = self.uac_json_e.copy()
        del uac_json['collectionExercise']['name']
        self.verify_missing(uac_json, 'No collection name supplied in UAC context JSON')

    def test_create_eq_constructor_missing_collection_case_ref(self):
        uac_json = self.uac_json_e.copy()
        del uac_json['collectionCase']['caseRef']
        self.verify_missing(uac_json, 'No caseRef supplied in UAC context JSON')

    def test_create_eq_constructor_missing_survey_url(self):
        uac_json = self.uac_json_e.copy()
        del uac_json['collectionInstrumentUrl']
        self.verify_missing(uac_json, 'No collectionInstrumentUrl in UAC context JSON')

    @unittest_run_loop
    async def test_build_en(self):
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
        self.maxDiff = None  # for full payload comparison when running this test
        with mock.patch('app.eq.uuid4') as mocked_uuid4, mock.patch(
                'app.eq.time.time') as mocked_time:
            # NB: has to be mocked after setup but before import
            mocked_time.return_value = self.eq_payload['iat']
            mocked_uuid4.return_value = self.jti

            with self.assertLogs('respondent-home', 'DEBUG') as cm:
                payload = await EqPayloadConstructor(self.uac_json_e,
                                                     self.attributes_en,
                                                     self.app).build()
            self.assertLogEvent(cm,
                                'creating payload for jwt',
                                case_id=self.case_id,
                                tx_id=self.jti)

        mocked_uuid4.assert_called()
        mocked_time.assert_called()
        self.assertEqual(payload, eq_payload)

    @unittest_run_loop
    async def test_build_cy(self):
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
        self.maxDiff = None  # for full payload comparison when running this test
        with mock.patch('app.eq.uuid4') as mocked_uuid4, mock.patch(
                'app.eq.time.time') as mocked_time:
            # NB: has to be mocked after setup but before import
            mocked_time.return_value = self.eq_payload['iat']
            mocked_uuid4.return_value = self.jti

            with self.assertLogs('respondent-home', 'DEBUG') as cm:
                payload = await EqPayloadConstructor(self.uac_json_w,
                                                     self.attributes_cy,
                                                     self.app).build()
            self.assertLogEvent(cm,
                                'creating payload for jwt',
                                case_id=self.case_id,
                                tx_id=self.jti)

        mocked_uuid4.assert_called()
        mocked_time.assert_called()
        self.assertEqual(payload, eq_payload)

    @unittest_run_loop
    async def test_build_raises_InvalidEqPayLoad_missing_attributes(self):

        from app import eq  # NB: local import to avoid overwriting the patched version for some tests

        with self.assertRaises(InvalidEqPayLoad) as ex:
            await eq.EqPayloadConstructor(self.uac_json_e, None, self.app).build()
        self.assertIn('Attributes is empty', ex.exception.message)

    def test_build_display_address_en(self):
        eq_payload = self.eq_payload.copy()
        eq_payload['region_code'] = 'GB-ENG'
        from app import eq

        result = eq.EqPayloadConstructor.build_display_address(
            self.uac_json_e['collectionCase']['sample'])
        self.assertEqual(result, eq_payload['display_address'])

    def test_build_display_address_cy(self):
        eq_payload = self.eq_payload.copy()
        eq_payload['region_code'] = 'GB-WLS'
        from app import eq

        result = eq.EqPayloadConstructor.build_display_address(
            self.uac_json_e['collectionCase']['sample'])
        self.assertEqual(result, eq_payload['display_address'])

    def test_convert_region_code_e(self):
        eq_payload = self.eq_payload.copy()
        eq_payload['region_code'] = 'GB-ENG'
        from app import eq

        result = eq.EqPayloadConstructor.convert_region_code(
            self.uac_json_e['collectionCase']['sample']['region'])
        self.assertEqual(result, eq_payload['region_code'])

    def test_convert_region_code_w(self):
        eq_payload = self.eq_payload.copy()
        eq_payload['region_code'] = 'GB-WLS'
        from app import eq

        result = eq.EqPayloadConstructor.convert_region_code(
            self.uac_json_w['collectionCase']['sample']['region'])
        self.assertEqual(result, eq_payload['region_code'])

    def test_build_display_address_raises(self):
        from app import eq

        attributes = {}

        with self.assertRaises(InvalidEqPayLoad) as ex:
            eq.EqPayloadConstructor.build_display_address(attributes)
            self.assertIn('Displayable address not in sample attributes',
                          ex.exception.message)

    def test_build_display_address_prems(self):
        from app import eq

        for attributes, expected in [
            ({
                'addressLine1': 'A House',
                'addressLine2': '',
            }, 'A House'),
            ({
                'addressLine1': '',
                'addressLine2': 'A Second House',
            }, 'A Second House'),
            ({
                'addressLine1': 'A House',
                'addressLine2': 'On The Second Hill',
            }, 'A House, On The Second Hill'),
            ({
                'addressLine1': 'Another House',
                'addressLine2': '',
                'addressLine3': '',
                'townName': '',
                'postcode': 'AA1 2BB'
            }, 'Another House, AA1 2BB'),
            ({
                'addressLine1': 'Another House',
                'addressLine2': '',
                'addressLine3': '',
                'townName': 'In Brizzle',
                'postcode': ''
            }, 'Another House, In Brizzle'),
            ({
                'addressLine1': 'Another House',
                'addressLine2': '',
                'addressLine3': 'In The Shire',
                'townName': '',
                'postcode': ''
            }, 'Another House, In The Shire'),
        ]:
            self.assertEqual(
                eq.EqPayloadConstructor.build_display_address(attributes),
                expected)
