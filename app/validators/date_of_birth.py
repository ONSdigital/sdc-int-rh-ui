from datetime import datetime
from app.exceptions import InvalidDataError


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
