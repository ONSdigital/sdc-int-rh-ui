from aiohttp.test_utils import unittest_run_loop
from app.eq import EqLaunch
from app.exceptions import InvalidEqPayLoad

from . import RHTestCase


class TestEq(RHTestCase):
    def test_create_eq_constructor(self):
        self.assertIsInstance(
            EqLaunch(self.uac_json_e, self.attributes_en, self.app), EqLaunch)

    def verify_missing(self, uac_json, expected_msg):
        with self.assertRaises(InvalidEqPayLoad) as ex:
            EqLaunch(uac_json, self.attributes_en, self.app)
        self.assertIn(expected_msg, ex.exception.message)

    def test_create_eq_constructor_missing_region(self):
        uac_json = self.uac_json_e.copy()
        del uac_json['collectionCase']['sample']['region']
        self.verify_missing(uac_json, 'Could not retrieve region from UAC context JSON')

    @unittest_run_loop
    async def test_url_path_en(self):
        url_path = EqLaunch(self.uac_json_e,
                            self.attributes_en,
                            self.app).url_path()
        self.assertRegex(url_path, '^/uacs/' + self.uacHash + '/launch')
        self.assertRegex(url_path, r'/launch\?languageCode=en')
        self.assertRegex(url_path, r'\&accountServiceUrl=' + self.app['ACCOUNT_SERVICE_URL'] + '/en/start/')
        self.assertRegex(url_path, r'\&accountServiceLogoutUrl=' + self.app['ACCOUNT_SERVICE_URL'] + '/en/signed-out/')

    @unittest_run_loop
    async def test_url_path_cy(self):
        url_path = EqLaunch(self.uac_json_w,
                            self.attributes_cy,
                            self.app).url_path()
        self.assertRegex(url_path, r'/launch\?languageCode=cy')
