import re
from app.exceptions import InvalidDataError, InvalidDataErrorWelsh


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
