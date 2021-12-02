from app.utils import FlashMessage, View

from . import RHTestCase


class TestUtils(RHTestCase):
    def test_generate_flash_message(self):
        built = FlashMessage.generate_flash_message('Test message', 'LEVEL', 'MESSAGE_TYPE', 'field')
        expected = {'text': 'Test message', 'level': 'LEVEL', 'type': 'MESSAGE_TYPE', 'field': 'field'}
        self.assertEqual(built, expected)

    def test_get_call_centre_number(self):
        built_ew = View.get_contact_centre_number('en')
        built_cy = View.get_contact_centre_number('cy')
        expected_ew = '0800 141 2021'
        expected_cy = '0800 169 2021'
        self.assertEqual(built_ew, expected_ew)
        self.assertEqual(built_cy, expected_cy)
