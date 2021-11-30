import string

from app.exceptions import InvalidDataError, InvalidDataErrorWelsh
from app import validators

uk_prefix = '44'


class ProcessMobileNumber:

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
