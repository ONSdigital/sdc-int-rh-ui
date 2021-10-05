import aiohttp_jinja2
import json

from aiohttp.client_exceptions import (ClientResponseError)
from aiohttp.web import HTTPFound, RouteTableDef
from structlog import get_logger

from . import (NO_SELECTION_CHECK_MSG)

from .flash import flash
from .exceptions import TooManyRequestsRegister
from .security import invalidate
from .session import get_existing_session, get_session_value
from .utils import View, ProcessMobileNumber, InvalidDataError, InvalidDataErrorWelsh, \
    FlashMessage, ProcessName, ProcessDOB, RHService

logger = get_logger('respondent-home')
register_routes = RouteTableDef()

user_journey = 'register'
valid_registration_types = r'{request_type:\bperson\b}'


@register_routes.view(r'/' + View.valid_display_regions_en_only + '/' + user_journey + '/')
class Register(View):
    @aiohttp_jinja2.template('register.html')
    async def get(self, request):
        display_region = 'en'
        page_title = 'Take part in a survey'
        locale = 'en'
        self.log_entry(request, display_region + '/' + user_journey)

        return {
            'display_region': display_region,
            'page_title': page_title,
            'locale': locale,
            'page_url': View.gen_page_url(request),
            'request_type': 'person'
        }


@register_routes.view(r'/' + View.valid_display_regions_en_only + '/' + user_journey + '/sis/')
class RegisterSIS(View):
    @aiohttp_jinja2.template('register-sis2.html')
    async def get(self, request):
        display_region = 'en'
        page_title = 'COVID-19 Schools Infection Survey (SIS)'
        locale = 'en'
        self.log_entry(request, display_region + '/' + user_journey + '/sis')

        return {
            'display_region': display_region,
            'page_title': page_title,
            'locale': locale,
            'page_url': View.gen_page_url(request),
            'request_type': 'person'
        }


@register_routes.view(r'/' + View.valid_display_regions_en_only + '/' + user_journey + '/school-list/')
class RegisterSchoolList(View):
    @aiohttp_jinja2.template('register-school-list.html')
    async def get(self, request):
        display_region = 'en'
        page_title = 'SIS school list'
        locale = 'en'
        self.log_entry(request, display_region + '/' + user_journey + '/school-list')

        school_list = []
        with open('app/data/schools.json') as file:
            data = json.load(file)
            for school in data:
                school_list.append({
                    'text': school['en']
                })

        return {
            'display_region': display_region,
            'page_title': page_title,
            'locale': locale,
            'page_url': View.gen_page_url(request),
            'request_type': 'person',
            'school_list': school_list
        }


@register_routes.view(r'/' + View.valid_display_regions_en_only + '/' + user_journey + '/' +
                      valid_registration_types + '/start/')
class RegisterStart(View):
    @aiohttp_jinja2.template('register-start.html')
    async def get(self, request):
        display_region = 'en'
        request_type = request.match_info['request_type']
        page_title = 'Start registration'
        locale = 'en'
        self.log_entry(request, display_region + '/' + user_journey + '/' + request_type + '/start')

        return {
            'display_region': display_region,
            'page_title': page_title,
            'locale': locale,
            'page_url': View.gen_page_url(request),
            'request_type': 'person'
        }

    async def post(self, request):
        display_region = request.match_info['display_region']
        request_type = request.match_info['request_type']
        self.log_entry(request, display_region + '/' + user_journey + '/' + request_type + '/start')

        session = await get_existing_session(request, user_journey, request_type)

        register_attributes = {
            'child_first_name': '',
            'child_middle_names': '',
            'child_last_name': '',
            'school_name': '',
            'child_dob_day': '',
            'child_dob_month': '',
            'child_dob_year': ''
        }
        session['register_attributes'] = register_attributes
        session.changed()
        raise HTTPFound(
            request.app.router['RegisterEnterName:get'].url_for(display_region=display_region,
                                                                request_type=request_type))


@register_routes.view(r'/' + View.valid_display_regions + '/' + user_journey + '/' + valid_registration_types +
                      '/enter-name/')
class RegisterEnterName(View):
    @aiohttp_jinja2.template('register-enter-name.html')
    async def get(self, request):

        request_type = request.match_info['request_type']
        display_region = request.match_info['display_region']

        page_title = "Enter name"
        if request.get('flash'):
            page_title = View.page_title_error_prefix_en + page_title
        locale = 'en'

        self.log_entry(request, display_region + '/' + user_journey + '/' + request_type + '/enter-name')

        await get_existing_session(request, user_journey, request_type)

        return {
            'page_title': page_title,
            'display_region': display_region,
            'locale': locale,
            'request_type': request_type,
            'page_url': View.gen_page_url(request)
        }

    async def post(self, request):
        request_type = request.match_info['request_type']
        display_region = request.match_info['display_region']

        self.log_entry(request, display_region + '/' + user_journey + '/' + request_type + '/enter-name')

        session = await get_existing_session(request, user_journey, request_type)
        register_attributes = get_session_value(request, session, 'register_attributes', user_journey, request_type)

        data = await request.post()

        form_valid = ProcessName.validate_name(request, data, display_region)

        if not form_valid:
            logger.info('form submission error',
                        client_ip=request['client_ip'],
                        client_id=request['client_id'],
                        trace=request['trace'],
                        region_of_site=display_region,
                        type_of_request=request_type)
            raise HTTPFound(
                request.app.router['RegisterEnterName:get'].url_for(
                    display_region=display_region,
                    request_type=request_type
                ))

        name_first_name = data['name_first_name'].strip()
        name_middle_names = data['name_middle_names'].strip()
        name_last_name = data['name_last_name'].strip()

        register_attributes['parent_first_name'] = name_first_name
        register_attributes['parent_middle_names'] = name_middle_names
        register_attributes['parent_last_name'] = name_last_name
        session.changed()

        raise HTTPFound(
            request.app.router['RegisterEnterMobile:get'].url_for(display_region=display_region,
                                                                  request_type=request_type))


@register_routes.view(r'/' + View.valid_display_regions + '/' + user_journey + '/' + valid_registration_types +
                      '/enter-mobile/')
class RegisterEnterMobile(View):
    @aiohttp_jinja2.template('register-enter-mobile.html')
    async def get(self, request):
        display_region = request.match_info['display_region']
        request_type = request.match_info['request_type']
        page_title = 'Enter mobile number'
        if request.get('flash'):
            page_title = View.page_title_error_prefix_en + page_title
        locale = 'en'

        self.log_entry(request, display_region + '/' + user_journey + '/' + request_type + '/enter-mobile')

        await get_existing_session(request, user_journey, request_type)

        return {
            'page_title': page_title,
            'display_region': display_region,
            'locale': locale,
            'page_url': View.gen_page_url(request)
        }

    async def post(self, request):
        display_region = request.match_info['display_region']
        request_type = request.match_info['request_type']
        locale = 'en'

        self.log_entry(request, display_region + '/' + user_journey + '/' + request_type + '/enter-mobile')

        session = await get_existing_session(request, user_journey, request_type)
        register_attributes = get_session_value(request, session, 'register_attributes', user_journey, request_type)

        data = await request.post()

        try:
            mobile_number = ProcessMobileNumber.validate_uk_mobile_phone_number(data['request-mobile-number'],
                                                                                locale)

            logger.info('valid mobile number',
                        client_ip=request['client_ip'], client_id=request['client_id'], trace=request['trace'])

            register_attributes['mobile_number'] = mobile_number
            register_attributes['submitted_mobile_number'] = data['request-mobile-number']
            session.changed()

            raise HTTPFound(
                request.app.router['RegisterConfirmMobile:get'].url_for(display_region=display_region,
                                                                        request_type=request_type))

        except (InvalidDataError, InvalidDataErrorWelsh) as exc:
            logger.info(exc, client_ip=request['client_ip'], client_id=request['client_id'], trace=request['trace'])
            if exc.message_type == 'empty':
                flash_message = FlashMessage.generate_flash_message(str(exc), 'ERROR', 'MOBILE_ENTER_ERROR',
                                                                    'mobile_empty')
            else:
                flash_message = FlashMessage.generate_flash_message(str(exc), 'ERROR', 'MOBILE_ENTER_ERROR',
                                                                    'mobile_invalid')
            flash(request, flash_message)
            raise HTTPFound(
                request.app.router['RegisterEnterMobile:get'].url_for(display_region=display_region,
                                                                      request_type=request_type))


@register_routes.view(r'/' + View.valid_display_regions + '/' + user_journey + '/' + valid_registration_types +
                      '/confirm-mobile/')
class RegisterConfirmMobile(View):
    @aiohttp_jinja2.template('register-confirm-mobile.html')
    async def get(self, request):
        display_region = request.match_info['display_region']
        request_type = request.match_info['request_type']
        self.log_entry(request, display_region + '/' + user_journey + '/' + request_type + '/confirm-mobile')

        session = await get_existing_session(request, user_journey, request_type)
        register_attributes = get_session_value(request, session, 'register_attributes', user_journey, request_type)

        page_title = 'Confirm your mobile'
        if request.get('flash'):
            page_title = View.page_title_error_prefix_en + page_title
        locale = 'en'

        return {
            'page_title': page_title,
            'display_region': display_region,
            'locale': locale,
            'page_url': View.gen_page_url(request),
            'submitted_mobile_number': get_session_value(request, register_attributes,
                                                         'submitted_mobile_number', user_journey)
        }

    async def post(self, request):
        display_region = request.match_info['display_region']
        request_type = request.match_info['request_type']
        self.log_entry(request, display_region + '/' + user_journey + '/' + request_type + '/confirm-mobile')

        await get_existing_session(request, user_journey, request_type)

        data = await request.post()
        try:
            mobile_confirmation = data['request-mobile-confirmation']
        except KeyError:
            logger.info('mobile confirmation error',
                        client_ip=request['client_ip'], client_id=request['client_id'], trace=request['trace'])
            flash(request, NO_SELECTION_CHECK_MSG)
            raise HTTPFound(
                request.app.router['RegisterConfirmMobile:get'].url_for(
                    display_region=display_region, request_type=request_type
                ))

        if mobile_confirmation == 'yes':
            raise HTTPFound(
                request.app.router['RegisterConsent:get'].url_for(display_region=display_region,
                                                                  request_type=request_type))

        elif mobile_confirmation == 'no':
            raise HTTPFound(
                request.app.router['RegisterEnterMobile:get'].url_for(display_region=display_region,
                                                                      request_type=request_type))

        else:
            # catch all just in case, should never get here
            logger.info('mobile confirmation error',
                        client_ip=request['client_ip'],
                        client_id=request['client_id'],
                        trace=request['trace'],
                        user_selection=mobile_confirmation)
            flash(request, NO_SELECTION_CHECK_MSG)
            raise HTTPFound(
                request.app.router['RegisterConfirmMobile:get'].url_for(display_region=display_region,
                                                                        request_type=request_type))


@register_routes.view(r'/' + View.valid_display_regions_en_only + '/' + user_journey + '/' +
                      valid_registration_types + '/consent/')
class RegisterConsent(View):
    @aiohttp_jinja2.template('register-consent.html')
    async def get(self, request):
        display_region = request.match_info['display_region']
        request_type = request.match_info['request_type']
        page_title = 'Confirm consent'
        locale = 'en'
        self.log_entry(request, display_region + '/' + user_journey + '/' + request_type + '/consent')

        await get_existing_session(request, user_journey, request_type)

        return {
            'display_region': display_region,
            'page_title': page_title,
            'locale': locale,
            'page_url': View.gen_page_url(request),
            'request_type': request_type
        }

    @aiohttp_jinja2.template('register-consent.html')
    async def post(self, request):
        display_region = request.match_info['display_region']
        request_type = request.match_info['request_type']
        self.log_entry(request, display_region + '/' + user_journey + '/' + request_type + '/consent')

        session = await get_existing_session(request, user_journey, request_type)
        register_attributes = get_session_value(request, session, 'register_attributes', user_journey, request_type)

        data = await request.post()
        logger.info(data)

        if data.get('button-decline') == 'decline':
            raise HTTPFound(
                request.app.router['RegisterConsentDeclined:get'].url_for(display_region=display_region,
                                                                          request_type=request_type))
        elif data.get('button-accept') == 'accept':
            register_attributes['consent'] = 'accept'
            session.changed()
            raise HTTPFound(
                request.app.router['RegisterEnterChildName:get'].url_for(display_region=display_region,
                                                                         request_type=request_type))
        else:
            raise HTTPFound(
                request.app.router['RegisterConsent:get'].url_for(display_region=display_region,
                                                                  request_type=request_type))


@register_routes.view(r'/' + View.valid_display_regions_en_only + '/' + user_journey + '/' + valid_registration_types +
                      '/consent-declined/')
class RegisterConsentDeclined(View):
    @aiohttp_jinja2.template('register-consent-declined.html')
    async def get(self, request):
        display_region = request.match_info['display_region']
        request_type = request.match_info['request_type']
        page_title = 'You have been removed from this study'
        locale = 'en'
        self.log_entry(request, display_region + '/' + user_journey + '/' + request_type + '/consent-declined')

        await invalidate(request)

        return {
            'display_region': display_region,
            'page_title': page_title,
            'locale': locale,
            'page_url': View.gen_page_url(request),
        }


@register_routes.view(r'/' + View.valid_display_regions + '/' + user_journey + '/' + valid_registration_types +
                      '/enter-child-name/')
class RegisterEnterChildName(View):
    @aiohttp_jinja2.template('register-enter-child-name.html')
    async def get(self, request):

        request_type = request.match_info['request_type']
        display_region = request.match_info['display_region']

        page_title = "Enter child name"
        if request.get('flash'):
            page_title = View.page_title_error_prefix_en + page_title
        locale = 'en'

        self.log_entry(request, display_region + '/' + user_journey + '/' + request_type + '/enter-child-name')

        session = await get_existing_session(request, user_journey, request_type)
        register_attributes = get_session_value(request, session, 'register_attributes', user_journey, request_type)

        return {
            'page_title': page_title,
            'display_region': display_region,
            'locale': locale,
            'request_type': request_type,
            'page_url': View.gen_page_url(request),
            'first_name': get_session_value(request, register_attributes, 
                                            'child_first_name', user_journey, request_type),
            'middle_names': get_session_value(request, register_attributes,
                                              'child_middle_names', user_journey, request_type),
            'last_name': get_session_value(request, register_attributes, 
                                           'child_last_name', user_journey, request_type)
        }

    async def post(self, request):
        request_type = request.match_info['request_type']
        display_region = request.match_info['display_region']

        self.log_entry(request, display_region + '/' + user_journey + '/' + request_type + '/enter-child-name')

        session = await get_existing_session(request, user_journey, request_type)
        register_attributes = get_session_value(request, session, 'register_attributes', user_journey, request_type)

        if (get_session_value(request, register_attributes, 'child_first_name', user_journey, request_type) == '' and
                get_session_value(request, register_attributes, 'child_last_name', user_journey, request_type) == ''):
            journey = 'new'
        else:
            journey = 'change'

        data = await request.post()

        form_valid = ProcessName.validate_name(request, data, display_region, child=True)

        if not form_valid:
            logger.info('form submission error',
                        client_ip=request['client_ip'],
                        client_id=request['client_id'],
                        trace=request['trace'],
                        region_of_site=display_region,
                        type_of_request=request_type)
            raise HTTPFound(
                request.app.router['RegisterEnterChildName:get'].url_for(
                    display_region=display_region,
                    request_type=request_type
                ))

        name_first_name = data['name_first_name'].strip()
        name_middle_names = data['name_middle_names'].strip()
        name_last_name = data['name_last_name'].strip()

        register_attributes['child_first_name'] = name_first_name
        register_attributes['child_middle_names'] = name_middle_names
        register_attributes['child_last_name'] = name_last_name
        session.changed()

        if journey == 'new':
            raise HTTPFound(
                request.app.router['RegisterSelectSchool:get'].url_for(display_region=display_region,
                                                                       request_type=request_type))
        else:
            raise HTTPFound(
                request.app.router['RegisterChildSummary:get'].url_for(display_region=display_region,
                                                                       request_type=request_type))


@register_routes.view(r'/' + View.valid_display_regions_en_only + '/' + user_journey + '/' +
                      valid_registration_types + '/select-school/')
class RegisterSelectSchool(View):
    @aiohttp_jinja2.template('register-select-school.html')
    async def get(self, request):
        display_region = request.match_info['display_region']
        request_type = request.match_info['request_type']
        page_title = 'Select school'
        if request.get('flash'):
            page_title = View.page_title_error_prefix_en + page_title
        locale = 'en'
        self.log_entry(request, display_region + '/' + user_journey + '/' + request_type + '/select-school')

        session = await get_existing_session(request, user_journey, request_type)
        register_attributes = get_session_value(request, session, 'register_attributes', user_journey, request_type)
        
        return {
            'display_region': display_region,
            'page_title': page_title,
            'locale': locale,
            'page_url': View.gen_page_url(request),
            'request_type': request_type,
            'first_name': get_session_value(request, register_attributes,
                                            'child_first_name', user_journey, request_type),
            'middle_names': get_session_value(request, register_attributes,
                                              'child_middle_names', user_journey, request_type),
            'last_name': get_session_value(request, register_attributes, 'child_last_name', user_journey, request_type),
            'school_name': get_session_value(request, register_attributes, 'school_name', user_journey, request_type)
        }

    async def post(self, request):
        display_region = request.match_info['display_region']
        request_type = request.match_info['request_type']
        self.log_entry(request, display_region + '/' + user_journey + '/' + request_type + '/select-school')

        session = await get_existing_session(request, user_journey, request_type)
        register_attributes = get_session_value(request, session, 'register_attributes', user_journey, request_type)

        if get_session_value(request, register_attributes, 'school_name', user_journey, request_type) == '':
            journey = 'new'
        else:
            journey = 'change'

        data = await request.post()

        if data.get('school-selection') and data.get('school-selection') != '':
            register_attributes['school_name'] = data.get('school-selection')
            session.changed()
            if journey == 'new':
                raise HTTPFound(
                    request.app.router['RegisterChildDOB:get'].url_for(display_region=display_region,
                                                                       request_type=request_type))
            else:
                raise HTTPFound(
                    request.app.router['RegisterChildSummary:get'].url_for(display_region=display_region,
                                                                           request_type=request_type))
        else:
            flash(request, {'text': 'Enter a value', 'level': 'ERROR', 'type': 'SCHOOL_ENTER_ERROR',
                            'field': 'error_selection'})
            raise HTTPFound(
                request.app.router['RegisterSelectSchool:get'].url_for(display_region=display_region,
                                                                       request_type=request_type))


@register_routes.view(r'/' + View.valid_display_regions + '/' + user_journey + '/' + valid_registration_types +
                      '/child-dob/')
class RegisterChildDOB(View):
    @aiohttp_jinja2.template('register-child-dob.html')
    async def get(self, request):

        request_type = request.match_info['request_type']
        display_region = request.match_info['display_region']

        page_title = "Enter date of birth"
        if request.get('flash'):
            page_title = View.page_title_error_prefix_en + page_title
        locale = 'en'

        self.log_entry(request, display_region + '/' + user_journey + '/' + request_type + '/child-dob')

        session = await get_existing_session(request, user_journey, request_type)
        register_attributes = get_session_value(request, session, 'register_attributes', user_journey, request_type)

        return {
            'page_title': page_title,
            'display_region': display_region,
            'locale': locale,
            'request_type': request_type,
            'page_url': View.gen_page_url(request),
            'first_name': get_session_value(request, register_attributes,
                                            'child_first_name', user_journey, request_type),
            'middle_names': get_session_value(request, register_attributes,
                                              'child_middle_names', user_journey, request_type),
            'last_name': get_session_value(request, register_attributes, 'child_last_name', user_journey, request_type),
            'day': get_session_value(request, register_attributes, 'child_dob_day', user_journey, request_type),
            'month': get_session_value(request, register_attributes, 'child_dob_month', user_journey, request_type),
            'year': get_session_value(request, register_attributes, 'child_dob_year', user_journey, request_type)
        }

    async def post(self, request):
        request_type = request.match_info['request_type']
        display_region = request.match_info['display_region']

        self.log_entry(request, display_region + '/' + user_journey + '/' + request_type + '/child-dob')

        session = await get_existing_session(request, user_journey, request_type)
        register_attributes = get_session_value(request, session, 'register_attributes', user_journey, request_type)

        data = await request.post()

        try:
            date = ProcessDOB.validate_dob(data)

            logger.info('valid dob',
                        client_ip=request['client_ip'], client_id=request['client_id'], trace=request['trace'])
            logger.info(date)

            register_attributes['child_dob_day'] = data.get('day')
            register_attributes['child_dob_month'] = data.get('month')
            register_attributes['child_dob_year'] = data.get('year')
            register_attributes['child_dob'] = str(date)
            session.changed()

            raise HTTPFound(
                request.app.router['RegisterChildSummary:get'].url_for(display_region=display_region,
                                                                       request_type=request_type))

        except InvalidDataError as exc:
            logger.info(exc, client_ip=request['client_ip'], client_id=request['client_id'], trace=request['trace'])
            flash_message = FlashMessage.generate_flash_message('Enter a valid date', 'ERROR', 'CHILD_DOB_ERROR',
                                                                'dob_invalid')
            flash(request, flash_message)
            raise HTTPFound(
                request.app.router['RegisterChildDOB:get'].url_for(display_region=display_region,
                                                                   request_type=request_type))


@register_routes.view(r'/' + View.valid_display_regions + '/' + user_journey + '/' + valid_registration_types +
                      '/child-summary/')
class RegisterChildSummary(View):
    @aiohttp_jinja2.template('register-child-summary.html')
    async def get(self, request):
        request_type = request.match_info['request_type']
        display_region = request.match_info['display_region']

        self.log_entry(request, display_region + '/' + user_journey + '/' + request_type + '/child-summary')

        session = await get_existing_session(request, user_journey, request_type)
        register_attributes = get_session_value(request, session, 'register_attributes', user_journey, request_type)

        page_title = 'Child summary'
        locale = 'en'

        return {
            'page_title': page_title,
            'display_region': display_region,
            'locale': locale,
            'request_type': request_type,
            'page_url': View.gen_page_url(request),
            'first_name': get_session_value(request, register_attributes,
                                            'child_first_name', user_journey, request_type),
            'middle_names': get_session_value(request, register_attributes,
                                              'child_middle_names', user_journey, request_type),
            'last_name': get_session_value(request, register_attributes, 'child_last_name', user_journey, request_type),
            'school_name': get_session_value(request, register_attributes, 'school_name', user_journey, request_type),
            'child_dob': ProcessDOB.format_dob(get_session_value(request, register_attributes, 'child_dob',
                                                                 user_journey, request_type))
        }

    async def post(self, request):
        display_region = request.match_info['display_region']
        request_type = request.match_info['request_type']
        self.log_entry(request, display_region + '/' + user_journey + '/' + request_type + '/child-summary')

        # TODO Trigger RHSvc endpoint

        raise HTTPFound(
            request.app.router['RegisterComplete:get'].url_for(display_region=display_region,
                                                               request_type=request_type))


@register_routes.view(r'/' + View.valid_display_regions + '/' + user_journey + '/' + valid_registration_types +
                      '/complete/')
class RegisterComplete(View):
    @aiohttp_jinja2.template('register-complete.html')
    async def get(self, request):
        request_type = request.match_info['request_type']
        display_region = request.match_info['display_region']

        self.log_entry(request, display_region + '/' + user_journey + '/' + request_type + '/complete')

        session = await get_existing_session(request, user_journey, request_type)
        register_attributes = get_session_value(request, session, 'register_attributes', user_journey, request_type)

        page_title = 'Registration complete'
        locale = 'en'

        await invalidate(request)

        return {
            'page_title': page_title,
            'display_region': display_region,
            'locale': locale,
            'request_type': request_type,
            'page_url': View.gen_page_url(request),
            'submitted_mobile_number': get_session_value(request, register_attributes,
                                                         'submitted_mobile_number', user_journey, request_type)
        }
