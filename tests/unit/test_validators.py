from app.validators.postcode import ProcessPostcode
from app.validators.mobile import ProcessMobileNumber
from app.exceptions import InvalidDataError, InvalidDataErrorWelsh

from . import RHTestCase


class TestValidatorsPostcode(RHTestCase):

    def test_validate_postcode_valid(self):
        postcode = 'PO15 5RR'
        locale = 'en'

        # When validate_postcode is called
        ProcessPostcode.validate_postcode(postcode, locale)
        # Nothing happens

    def test_validate_postcode_valid_with_unicode(self):
        postcode = 'BS２ ０FW'
        locale = 'en'

        # When validate_postcode is called
        ProcessPostcode.validate_postcode(postcode, locale)
        # Nothing happens

    def test_validate_postcode_empty(self):
        postcode = ''
        locale = 'en'

        # When validate_postcode is called
        with self.assertRaises(InvalidDataError) as cm:
            ProcessPostcode.validate_postcode(postcode, locale)
        # Then an InvalidDataError is raised
        self.assertEqual(
            'Enter a postcode',
            str(cm.exception)
        )
        # With the correct message

    def test_validate_postcode_not_alphanumeric(self):
        postcode = '?<>:{}'
        locale = 'en'

        # When validate_postcode is called
        with self.assertRaises(InvalidDataError) as cm:
            ProcessPostcode.validate_postcode(postcode, locale)
        # Then an InvalidDataError is raised
        self.assertEqual(
            'Enter a valid UK postcode',
            str(cm.exception)
        )
        # With the correct message

    def test_validate_postcode_short(self):
        postcode = 'PO15'
        locale = 'en'

        # When validate_postcode is called
        with self.assertRaises(InvalidDataError) as cm:
            ProcessPostcode.validate_postcode(postcode, locale)
        # Then an InvalidDataError is raised
        self.assertEqual(
            'Enter a valid UK postcode',
            str(cm.exception)
        )
        # With the correct message

    def test_validate_postcode_long(self):
        postcode = 'PO15 5RRR'
        locale = 'en'

        # When validate_postcode is called
        with self.assertRaises(InvalidDataError) as cm:
            ProcessPostcode.validate_postcode(postcode, locale)
        # Then an InvalidDataError is raised
        self.assertEqual(
            'Enter a valid UK postcode',
            str(cm.exception)
        )
        # With the correct message

    def test_validate_postcode_invalid(self):
        postcode = 'ZZ99 9ZZ'
        locale = 'en'

        # When validate_postcode is called
        with self.assertRaises(InvalidDataError) as cm:
            ProcessPostcode.validate_postcode(postcode, locale)
        # Then an InvalidDataError is raised
        self.assertEqual(
            'Enter a valid UK postcode',
            str(cm.exception)
        )
        # With the correct message

    def test_validate_postcode_valid_cy(self):
        postcode = 'PO15 5RR'
        locale = 'cy'

        # When validate_postcode is called
        ProcessPostcode.validate_postcode(postcode, locale)
        # Nothing happens

    def test_validate_postcode_empty_cy(self):
        postcode = ''
        locale = 'cy'

        # When validate_postcode is called
        with self.assertRaises(InvalidDataErrorWelsh) as cm:
            ProcessPostcode.validate_postcode(postcode, locale)
        # Then an InvalidDataError is raised
        self.assertEqual(
            'Rhowch god post',
            str(cm.exception)
        )
        # With the correct message

    def test_validate_postcode_not_alphanumeric_cy(self):
        postcode = '?<>:{}'
        locale = 'cy'

        # When validate_postcode is called
        with self.assertRaises(InvalidDataErrorWelsh) as cm:
            ProcessPostcode.validate_postcode(postcode, locale)
        # Then an InvalidDataError is raised
        self.assertEqual(
            'Rhowch god post dilys yn y Deyrnas Unedig',
            str(cm.exception)
        )
        # With the correct message

    def test_validate_postcode_short_cy(self):
        postcode = 'PO15'
        locale = 'cy'

        # When validate_postcode is called
        with self.assertRaises(InvalidDataErrorWelsh) as cm:
            ProcessPostcode.validate_postcode(postcode, locale)
        # Then an InvalidDataError is raised
        self.assertEqual(
            'Rhowch god post dilys yn y Deyrnas Unedig',
            str(cm.exception)
        )
        # With the correct message

    def test_validate_postcode_long_cy(self):
        postcode = 'PO15 5RRR'
        locale = 'cy'

        # When validate_postcode is called
        with self.assertRaises(InvalidDataErrorWelsh) as cm:
            ProcessPostcode.validate_postcode(postcode, locale)
        # Then an InvalidDataError is raised
        self.assertEqual(
            'Rhowch god post dilys yn y Deyrnas Unedig',
            str(cm.exception)
        )
        # With the correct message

    def test_validate_postcode_invalid_cy(self):
        postcode = 'ZZ99 9ZZ'
        locale = 'cy'

        # When validate_postcode is called
        with self.assertRaises(InvalidDataErrorWelsh) as cm:
            ProcessPostcode.validate_postcode(postcode, locale)
        # Then an InvalidDataError is raised
        self.assertEqual(
            'Rhowch god post dilys yn y Deyrnas Unedig',
            str(cm.exception)
        )
        # With the correct message

    def test_validate_postcode_invalid_BritishForces(self):
        postcode = 'BFPO 105'
        locale = 'en'

        # When validate_postcode is called
        with self.assertRaises(InvalidDataError) as cm:
            ProcessPostcode.validate_postcode(postcode, locale)
        # Then an InvalidDataError is raised
        self.assertEqual(
            'Enter a valid UK postcode',
            str(cm.exception)
        )
        # With the correct message


class TestValidatorsMobile(RHTestCase):
    def test_validate_uk_mobile_phone_number_valid(self):
        mobile_number = '070 1234 5678'
        locale = 'en'

        # When validate_uk_mobile_phone_number is called
        ProcessMobileNumber.validate_uk_mobile_phone_number(mobile_number, locale)
        # Nothing happens

    def test_validate_uk_mobile_phone_number_short(self):
        mobile_number = '070 1234'
        locale = 'en'

        # When validate_uk_mobile_phone_number is called
        with self.assertRaises(InvalidDataError) as cm:
            ProcessMobileNumber.validate_uk_mobile_phone_number(mobile_number, locale)
        # Then an InvalidDataError is raised
        self.assertEqual(
            self.content_common_invalid_mobile_error_en,
            str(cm.exception)
        )
        # With the correct message

    def test_validate_uk_mobile_phone_number_long(self):
        mobile_number = '070 1234 5678 9012 3456 7890'
        locale = 'en'

        # When validate_uk_mobile_phone_number is called
        with self.assertRaises(InvalidDataError) as cm:
            ProcessMobileNumber.validate_uk_mobile_phone_number(mobile_number, locale)
        # Then an InvalidDataError is raised
        self.assertEqual(
            self.content_common_invalid_mobile_error_en,
            str(cm.exception)
        )
        # With the correct message

    def test_validate_uk_mobile_phone_number_not_mobile(self):
        mobile_number = '020 1234 5678'
        locale = 'en'

        # When validate_uk_mobile_phone_number is called
        with self.assertRaises(InvalidDataError) as cm:
            ProcessMobileNumber.validate_uk_mobile_phone_number(mobile_number, locale)
        # Then an InvalidDataError is raised
        self.assertEqual(
            self.content_common_invalid_mobile_error_en,
            str(cm.exception)
        )
        # With the correct message

    def test_validate_uk_mobile_phone_number_not_numeric(self):
        mobile_number = 'gdsjkghjdsghjsd'
        locale = 'en'

        # When validate_uk_mobile_phone_number is called
        with self.assertRaises(InvalidDataError) as cm:
            ProcessMobileNumber.validate_uk_mobile_phone_number(mobile_number, locale)
        # Then an InvalidDataError is raised
        self.assertEqual(
            self.content_common_invalid_mobile_error_en,
            str(cm.exception)
        )
        # With the correct message

    def test_validate_uk_mobile_phone_number_valid_cy(self):
        mobile_number = '070 1234 5678'
        locale = 'cy'

        # When validate_uk_mobile_phone_number is called
        ProcessMobileNumber.validate_uk_mobile_phone_number(mobile_number, locale)
        # Nothing happens

    def test_validate_uk_mobile_phone_number_short_cy(self):
        mobile_number = '070 1234'
        locale = 'cy'

        # When validate_uk_mobile_phone_number is called
        with self.assertRaises(InvalidDataErrorWelsh) as cm:
            ProcessMobileNumber.validate_uk_mobile_phone_number(mobile_number, locale)
        # Then an InvalidDataError is raised
        self.assertEqual(
            self.content_common_invalid_mobile_error_cy,
            str(cm.exception)
        )
        # With the correct message

    def test_validate_uk_mobile_phone_number_long_cy(self):
        mobile_number = '070 1234 5678 9012 3456 7890'
        locale = 'cy'

        # When validate_uk_mobile_phone_number is called
        with self.assertRaises(InvalidDataErrorWelsh) as cm:
            ProcessMobileNumber.validate_uk_mobile_phone_number(mobile_number, locale)
        # Then an InvalidDataError is raised
        self.assertEqual(
            self.content_common_invalid_mobile_error_cy,
            str(cm.exception)
        )
        # With the correct message

    def test_validate_uk_mobile_phone_number_not_mobile_cy(self):
        mobile_number = '020 1234 5678'
        locale = 'cy'

        # When validate_uk_mobile_phone_number is called
        with self.assertRaises(InvalidDataErrorWelsh) as cm:
            ProcessMobileNumber.validate_uk_mobile_phone_number(mobile_number, locale)
        # Then an InvalidDataError is raised
        self.assertEqual(
            self.content_common_invalid_mobile_error_cy,
            str(cm.exception)
        )
        # With the correct message

    def test_validate_uk_mobile_phone_number_not_numeric_cy(self):
        mobile_number = 'gdsjkghjdsghjsd'
        locale = 'cy'

        # When validate_uk_mobile_phone_number is called
        with self.assertRaises(InvalidDataErrorWelsh) as cm:
            ProcessMobileNumber.validate_uk_mobile_phone_number(mobile_number, locale)
        # Then an InvalidDataError is raised
        self.assertEqual(
            self.content_common_invalid_mobile_error_cy,
            str(cm.exception)
        )
        # With the correct message
