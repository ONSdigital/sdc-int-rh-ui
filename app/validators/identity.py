import string
import re

from app.flash import flash
from datetime import datetime

from app.exceptions import InvalidDataError, InvalidDataErrorWelsh
from app import validators

uk_prefix = '44'


class IdentityValidators:
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

    @staticmethod
    def normalise_phone_number(number, locale):

        for character in string.whitespace + validators.OBSCURE_WHITESPACE + '()-+':
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

        number = IdentityValidators.normalise_phone_number(number, locale).lstrip(uk_prefix).lstrip('0')

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
            if IdentityValidators.email_validation_pattern.fullmatch(email):
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
