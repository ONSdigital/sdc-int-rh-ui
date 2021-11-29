import string
import re

from aiohttp.client_exceptions import (ClientResponseError)
from .exceptions import InvalidDataError, InvalidDataErrorWelsh, TooManyRequestsEQLaunch
from aiohttp.web import HTTPFound
from datetime import datetime
from pytz import timezone
from unicodedata import normalize

from app.comms.rhsvc import EQLaunch

from sdc.crypto.encrypter import encrypt
from .eq import EqPayloadConstructor
from .flash import flash
from structlog import get_logger

logger = get_logger('respondent-home')

OBSCURE_WHITESPACE = (
    '\u180E'  # Mongolian vowel separator
    '\u200B'  # zero width space
    '\u200C'  # zero width non-joiner
    '\u200D'  # zero width joiner
    '\u2060'  # word joiner
    '\uFEFF'  # zero width non-breaking space
)

uk_prefix = '44'
uk_zone = timezone('Europe/London')


class View:
    valid_display_regions = r'{display_region:\ben|cy\b}'
    valid_display_regions_en_only = r'{display_region:\ben\b}'
    valid_user_journeys = r'{user_journey:\bstart|request\b}'
    page_title_error_prefix_en = 'Error: '
    page_title_error_prefix_cy = 'Gwall: '

    @staticmethod
    def log_entry(request, endpoint):
        method = request.method
        logger.info(f"received {method} on endpoint '{endpoint}'",
                    client_ip=request['client_ip'],
                    client_id=request['client_id'],
                    trace=request['trace'],
                    method=request.method,
                    path=request.path)

    @staticmethod
    def gen_page_url(request):
        full_url = str(request.rel_url)
        if full_url[:3] == '/en' or full_url[:3] == '/cy':
            generic_url = full_url[3:]
        else:
            generic_url = full_url
        return generic_url

    @staticmethod
    def get_contact_centre_number(display_region):
        if display_region == 'cy':
            contact_centre_number = '0800 169 2021'
        else:
            contact_centre_number = '0800 141 2021'
        return contact_centre_number

    @staticmethod
    def get_campaign_site_link(request, display_region, requested_link):
        base_en = request.app['DOMAIN_URL_PROTOCOL'] + request.app['DOMAIN_URL_EN']
        base_cy = request.app['DOMAIN_URL_PROTOCOL'] + request.app['DOMAIN_URL_CY']

        link = '/'

        if requested_link == 'surveys-home':
            if display_region == 'cy':
                link = base_cy
            else:
                link = base_en
        elif requested_link == 'contact-us':
            if display_region == 'cy':
                link = base_cy + '/cysylltu-a-ni/'
            else:
                link = base_en + '/contact-us/'
        elif requested_link == 'privacy':
            if display_region == 'cy':
                link = base_cy + '/preifatrwydd-a-diogelu-data/'
            else:
                link = base_en + '/privacy-and-data-protection/'

        return link


class LaunchEQ:
    @staticmethod
    async def call_questionnaire(request, case, attributes, app, adlocation):
        eq_payload = await EqPayloadConstructor(case, attributes, app).build()

        token = encrypt(eq_payload,
                        key_store=app['key_store'],
                        key_purpose='authentication')

        try:
            await EQLaunch.post_surveylaunched(request, case, adlocation)
        except ClientResponseError as ex:
            if ex.status == 429:
                raise TooManyRequestsEQLaunch()
            else:
                raise ex

        logger.info('redirecting to eq',
                    client_ip=request['client_ip'], client_id=request['client_id'], trace=request['trace'])
        eq_url = app['EQ_URL']
        raise HTTPFound(f'{eq_url}/session?token={token}')


class ProcessPostcode:
    postcode_validation_pattern = re.compile(
        r'^((AB|AL|B|BA|BB|BD|BH|BL|BN|BR|BS|BT|BX|CA|CB|CF|CH|CM|CO|CR|CT|CV|CW|DA|DD|DE|DG|DH|DL|DN|DT|DY|E|EC|EH|EN|EX|FK|FY|G|GL|GY|GU|HA|HD|HG|HP|HR|HS|HU|HX|IG|IM|IP|IV|JE|KA|KT|KW|KY|L|LA|LD|LE|LL|LN|LS|LU|M|ME|MK|ML|N|NE|NG|NN|NP|NR|NW|OL|OX|PA|PE|PH|PL|PO|PR|RG|RH|RM|S|SA|SE|SG|SK|SL|SM|SN|SO|SP|SR|SS|ST|SW|SY|TA|TD|TF|TN|TQ|TR|TS|TW|UB|W|WA|WC|WD|WF|WN|WR|WS|WV|YO|ZE)(\d[\dA-Z]?[ ]?\d[ABD-HJLN-UW-Z]{2}))$'  # NOQA
    )

    @staticmethod
    def validate_postcode(postcode, locale):

        for character in string.whitespace + OBSCURE_WHITESPACE:
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

        if not ProcessPostcode.postcode_validation_pattern.fullmatch(postcode):
            if locale == 'cy':
                raise InvalidDataErrorWelsh("Rhowch god post dilys yn y Deyrnas Unedig")
            else:
                raise InvalidDataError('Enter a valid UK postcode')

        postcode_formatted = postcode[:-3] + ' ' + postcode[-3:]

        return postcode_formatted


class ProcessMobileNumber:

    @staticmethod
    def normalise_phone_number(number, locale):

        for character in string.whitespace + OBSCURE_WHITESPACE + '()-+':
            number = number.replace(character, '')

        try:
            list(map(int, number))
        except ValueError:
            if locale == 'cy':
                raise InvalidDataErrorWelsh("Rhowch rif ffôn symudol yn y Deyrnas Unedig mewn fformat dilys, "
                                            "er enghraifft, 07700 900345 neu +44 7700 900345", message_type='invalid')
            else:
                raise InvalidDataError('Enter a UK mobile number in a valid format, for example, '
                                       '07700 900345 or +44 7700 900345', message_type='invalid')

        return number.lstrip('0')

    @staticmethod
    def validate_uk_mobile_phone_number(number, locale):

        number = ProcessMobileNumber.normalise_phone_number(number, locale).lstrip(uk_prefix).lstrip('0')

        if len(number) == 0:
            if locale == 'cy':
                raise InvalidDataErrorWelsh("Rhowch eich rhif ffôn symudol", message_type='empty')
            else:
                raise InvalidDataError('Enter your mobile number', message_type='empty')

        if not number.startswith('7'):
            if locale == 'cy':
                raise InvalidDataErrorWelsh("Rhowch rif ffôn symudol yn y Deyrnas Unedig mewn fformat dilys, "
                                            "er enghraifft, 07700 900345 neu +44 7700 900345", message_type='invalid')
            else:
                raise InvalidDataError('Enter a UK mobile number in a valid format, for example, '
                                       '07700 900345 or +44 7700 900345', message_type='invalid')

        if len(number) > 10:
            if locale == 'cy':
                raise InvalidDataErrorWelsh("Rhowch rif ffôn symudol yn y Deyrnas Unedig mewn fformat dilys, "
                                            "er enghraifft, 07700 900345 neu +44 7700 900345", message_type='invalid')
            else:
                raise InvalidDataError('Enter a UK mobile number in a valid format, for example, '
                                       '07700 900345 or +44 7700 900345', message_type='invalid')

        if len(number) < 10:
            if locale == 'cy':
                raise InvalidDataErrorWelsh("Rhowch rif ffôn symudol yn y Deyrnas Unedig mewn fformat dilys, "
                                            "er enghraifft, 07700 900345 neu +44 7700 900345", message_type='invalid')
            else:
                raise InvalidDataError('Enter a UK mobile number in a valid format, for example, '
                                       '07700 900345 or +44 7700 900345', message_type='invalid')

        return '{}{}'.format(uk_prefix, number)


class ProcessName:

    @staticmethod
    def validate_name(request, data, display_region, child=False):

        name_valid = True
        form_first_name = data.get('name_first_name')
        form_last_name = data.get('name_last_name')

        if (not form_first_name) or (len(form_first_name.strip()) == 0):
            if child:
                flash(request, {'text': "Enter your child's first name", 'level': 'ERROR', 'type': 'NAME_ENTER_ERROR',
                                'field': 'error_first_name', 'value_first_name': form_first_name,
                                'value_last_name': form_last_name})
            else:
                if display_region == 'cy':
                    flash(request, {'text': "Rhowch eich enw cyntaf", 'level': 'ERROR', 'type': 'NAME_ENTER_ERROR',
                                    'field': 'error_first_name', 'value_first_name': form_first_name,
                                    'value_last_name': form_last_name})
                else:
                    flash(request, {'text': "Enter your first name", 'level': 'ERROR', 'type': 'NAME_ENTER_ERROR',
                                    'field': 'error_first_name', 'value_first_name': form_first_name,
                                    'value_last_name': form_last_name})
            name_valid = False

        elif len(form_first_name) > 35:
            if display_region == 'cy':
                flash(request, {'text': "Rydych wedi defnyddio gormod o nodau. Rhowch hyd at 35 o nodau",
                                'level': 'ERROR', 'type': 'NAME_ENTER_ERROR', 'field': 'error_first_name_len',
                                'value_first_name': form_first_name, 'value_last_name': form_last_name})
            else:
                flash(request, {'text': 'You have entered too many characters. Enter up to 35 characters',
                                'level': 'ERROR', 'type': 'NAME_ENTER_ERROR', 'field': 'error_first_name_len',
                                'value_first_name': form_first_name, 'value_last_name': form_last_name})
            name_valid = False

        if (not form_last_name) or (len(form_last_name.strip()) == 0):
            if child:
                flash(request, {'text': "Enter your child's last name", 'level': 'ERROR', 'type': 'NAME_ENTER_ERROR',
                                'field': 'error_last_name', 'value_first_name': form_first_name,
                                'value_last_name': form_last_name})
            else:
                if display_region == 'cy':
                    flash(request, {'text': "Rhowch eich cyfenw", 'level': 'ERROR', 'type': 'NAME_ENTER_ERROR',
                                    'field': 'error_last_name', 'value_first_name': form_first_name,
                                    'value_last_name': form_last_name})
                else:
                    flash(request, {'text': "Enter your last name", 'level': 'ERROR', 'type': 'NAME_ENTER_ERROR',
                                    'field': 'error_last_name', 'value_first_name': form_first_name,
                                    'value_last_name': form_last_name})
            name_valid = False

        elif len(form_last_name) > 35:
            if display_region == 'cy':
                flash(request, {'text': "Rydych wedi defnyddio gormod o nodau. Rhowch hyd at 35 o nodau",
                                'level': 'ERROR', 'type': 'NAME_ENTER_ERROR', 'field': 'error_last_name_len',
                                'value_first_name': form_first_name, 'value_last_name': form_last_name})
            else:
                flash(request, {'text': 'You have entered too many characters. Enter up to 35 characters',
                                'level': 'ERROR', 'type': 'NAME_ENTER_ERROR', 'field': 'error_last_name_len',
                                'value_first_name': form_first_name, 'value_last_name': form_last_name})
            name_valid = False

        return name_valid


class ProcessDOB:
    @staticmethod
    def validate_dob(data):
        form_day = data.get('day')
        form_month = data.get('month')
        form_year = data.get('year')

        try:
            date = datetime(int(form_year), int(form_month), int(form_day)).date()
            return date
        except ValueError:
            raise InvalidDataError('invalid dob', message_type='invalid')

    @staticmethod
    def format_dob(date_value):
        unformatted_date = datetime.strptime(date_value, '%Y-%m-%d')
        formatted_date = unformatted_date.strftime('%d %B %Y')
        return formatted_date


class ProcessEmailAddress:
    email_validation_pattern = re.compile(
        r'(^[^@\s]+@[^@\s]+\.[^@\s]+$)'
    )

    @staticmethod
    def validate_email(email, locale):
        if len(email.strip()) == 0:
            if locale == 'cy':
                raise InvalidDataErrorWelsh("Enter an email address", message_type='empty')
            else:
                raise InvalidDataError('Enter an email address', message_type='empty')
        else:
            if ProcessEmailAddress.email_validation_pattern.fullmatch(email):
                return email
            else:
                if locale == 'cy':
                    raise InvalidDataErrorWelsh(
                        "Enter an email address in a valid format, for example, name@example.com",
                        message_type='invalid')
                else:
                    raise InvalidDataError(
                        'Enter an email address in a valid format, for example, name@example.com',
                        message_type='invalid')


class FlashMessage:

    @staticmethod
    def generate_flash_message(text, level, message_type, field):
        json_return = {'text': text, 'level': level, 'type': message_type, 'field': field}
        return json_return
