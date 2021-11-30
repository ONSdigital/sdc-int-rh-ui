from app.flash import flash


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
