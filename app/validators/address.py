import re
import string

from unicodedata import normalize
from app.exceptions import InvalidDataError, InvalidDataErrorWelsh
from app import validators


class AddressValidators:
    postcode_validation_pattern = re.compile(
        r'^((AB|AL|B|BA|BB|BD|BH|BL|BN|BR|BS|BT|BX|CA|CB|CF|CH|CM|CO|CR|CT|CV|CW|DA|DD|DE|DG|DH|DL|DN|DT|DY|E|EC|EH|EN|EX|FK|FY|G|GL|GY|GU|HA|HD|HG|HP|HR|HS|HU|HX|IG|IM|IP|IV|JE|KA|KT|KW|KY|L|LA|LD|LE|LL|LN|LS|LU|M|ME|MK|ML|N|NE|NG|NN|NP|NR|NW|OL|OX|PA|PE|PH|PL|PO|PR|RG|RH|RM|S|SA|SE|SG|SK|SL|SM|SN|SO|SP|SR|SS|ST|SW|SY|TA|TD|TF|TN|TQ|TR|TS|TW|UB|W|WA|WC|WD|WF|WN|WR|WS|WV|YO|ZE)(\d[\dA-Z]?[ ]?\d[ABD-HJLN-UW-Z]{2}))$'  # NOQA
    )

    @staticmethod
    def validate_postcode(postcode, locale):

        for character in string.whitespace + validators.OBSCURE_WHITESPACE:
            postcode = postcode.replace(character, '')

        postcode = postcode.upper()
        postcode = normalize('NFKD', postcode).encode('ascii', 'ignore').decode('utf8')

        if len(postcode) == 0:
            if locale == 'cy':
                raise InvalidDataErrorWelsh("Rhowch god post", 'empty')
            else:
                raise InvalidDataError('Enter a postcode', 'empty')

        if not postcode.isalnum():
            if locale == 'cy':
                raise InvalidDataErrorWelsh("Rhowch god post dilys yn y Deyrnas Unedig")
            else:
                raise InvalidDataError('Enter a valid UK postcode')

        if len(postcode) < 5:
            if locale == 'cy':
                raise InvalidDataErrorWelsh("Rhowch god post dilys yn y Deyrnas Unedig")
            else:
                raise InvalidDataError('Enter a valid UK postcode')

        if len(postcode) > 7:
            if locale == 'cy':
                raise InvalidDataErrorWelsh("Rhowch god post dilys yn y Deyrnas Unedig")
            else:
                raise InvalidDataError('Enter a valid UK postcode')

        if not AddressValidators.postcode_validation_pattern.fullmatch(postcode):
            if locale == 'cy':
                raise InvalidDataErrorWelsh("Rhowch god post dilys yn y Deyrnas Unedig")
            else:
                raise InvalidDataError('Enter a valid UK postcode')

        postcode_formatted = postcode[:-3] + ' ' + postcode[-3:]

        return postcode_formatted
