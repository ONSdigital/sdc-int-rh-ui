import aiohttp_jinja2

from aiohttp.client_exceptions import (ClientResponseError)
from aiohttp.web import HTTPFound, RouteTableDef
from structlog import get_logger

from . import (NO_SELECTION_CHECK_MSG)

from .flash import flash
from .exceptions import TooManyRequestsRegister
from .security import invalidate
from .session import get_existing_session, get_session_value
from .utils import View, ProcessMobileNumber, InvalidDataError, InvalidDataErrorWelsh, \
    FlashMessage, ProcessName, RHService

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

        fulfilment_attributes = {
            'survey': 'sis2',
            'first_name': '',
            'middle_names': '',
            'last_name': ''
        }
        session['fulfilment_attributes'] = fulfilment_attributes
        session.changed()
        raise HTTPFound(
            request.app.router['RegisterEnterName:get'].url_for(display_region=display_region,
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
        fulfilment_attributes = get_session_value(request, session, 'fulfilment_attributes', user_journey, request_type)

        data = await request.post()
        logger.info(data)

        if data.get('button-decline') == 'decline':
            raise HTTPFound(
                request.app.router['RegisterConsentDeclined:get'].url_for(display_region=display_region,
                                                                          request_type=request_type))
        elif data.get('button-accept') == 'accept':
            fulfilment_attributes['consent'] = 'accept'
            session.changed()
            raise HTTPFound(
                request.app.router['RegisterEnterMobile:get'].url_for(display_region=display_region,
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
        fulfilment_attributes = get_session_value(request, session, 'fulfilment_attributes', user_journey, request_type)

        data = await request.post()

        try:
            mobile_number = ProcessMobileNumber.validate_uk_mobile_phone_number(data['request-mobile-number'],
                                                                                locale)

            logger.info('valid mobile number',
                        client_ip=request['client_ip'], client_id=request['client_id'], trace=request['trace'])

            fulfilment_attributes['mobile_number'] = mobile_number
            fulfilment_attributes['submitted_mobile_number'] = data['request-mobile-number']
            session.changed()

            raise HTTPFound(
                request.app.router['RegisterConfirmRegistration:get'].url_for(display_region=display_region,
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
                      '/confirm-registration/')
class RegisterConfirmRegistration(View):
    @aiohttp_jinja2.template('register-confirm-registration.html')
    async def get(self, request):
        display_region = request.match_info['display_region']
        request_type = request.match_info['request_type']
        self.log_entry(request, display_region + '/' + user_journey + '/' + request_type + '/confirm-registration')

        session = await get_existing_session(request, user_journey, request_type)
        fulfilment_attributes = get_session_value(request, session, 'fulfilment_attributes', user_journey, request_type)

        page_title = 'Confirm your registration'
        if request.get('flash'):
            page_title = View.page_title_error_prefix_en + page_title
        locale = 'en'

        return {
            'page_title': page_title,
            'display_region': display_region,
            'locale': locale,
            'page_url': View.gen_page_url(request),
            'submitted_mobile_number': get_session_value(request, fulfilment_attributes,
                                                         'submitted_mobile_number', user_journey)
        }

    async def post(self, request):
        display_region = request.match_info['display_region']
        request_type = request.match_info['request_type']
        self.log_entry(request, display_region + '/' + user_journey + '/' + request_type + '/confirm-registration')

        session = await get_existing_session(request, user_journey, request_type)
        fulfilment_attributes = get_session_value(request, session, 'fulfilment_attributes', user_journey, request_type)

        data = await request.post()
        try:
            mobile_confirmation = data['request-mobile-confirmation']
        except KeyError:
            logger.info('mobile confirmation error',
                        client_ip=request['client_ip'], client_id=request['client_id'], trace=request['trace'])
            flash(request, NO_SELECTION_CHECK_MSG)
            raise HTTPFound(
                request.app.router['RegisterConfirmRegistration:get'].url_for(
                    display_region=display_region, request_type=request_type
                ))

        if mobile_confirmation == 'yes':
            mobile_number = get_session_value(request, fulfilment_attributes, 'mobile_number',
                                              user_journey, request_type)

            # TODO RHSvc Register Person call

            raise HTTPFound(
                request.app.router['RegisterComplete:get'].url_for(display_region=display_region,
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
                request.app.router['RegisterConfirmRegistration:get'].url_for(display_region=display_region,
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
        fulfilment_attributes = get_session_value(request, session, 'fulfilment_attributes', user_journey, request_type)

        page_title = 'Registration complete'
        locale = 'en'

        await invalidate(request)

        return {
            'page_title': page_title,
            'display_region': display_region,
            'locale': locale,
            'request_type': request_type,
            'page_url': View.gen_page_url(request),
            'submitted_mobile_number': get_session_value(request, fulfilment_attributes,
                                                         'submitted_mobile_number', user_journey, request_type)
        }


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

        session = await get_existing_session(request, user_journey, request_type)
        fulfilment_attributes = get_session_value(request, session, 'fulfilment_attributes', user_journey, request_type)

        return {
            'page_title': page_title,
            'display_region': display_region,
            'locale': locale,
            'request_type': request_type,
            'page_url': View.gen_page_url(request),
            'first_name': get_session_value(request, fulfilment_attributes, 'first_name', user_journey, request_type),
            'middle_names': get_session_value(request, fulfilment_attributes,
                                              'middle_names', user_journey, request_type),
            'last_name': get_session_value(request, fulfilment_attributes, 'last_name', user_journey, request_type)
        }

    async def post(self, request):
        request_type = request.match_info['request_type']
        display_region = request.match_info['display_region']

        self.log_entry(request, display_region + '/' + user_journey + '/' + request_type + '/enter-name')

        session = await get_existing_session(request, user_journey, request_type)
        fulfilment_attributes = get_session_value(request, session, 'fulfilment_attributes', user_journey, request_type)

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

        fulfilment_attributes['first_name'] = name_first_name
        fulfilment_attributes['middle_names'] = name_middle_names
        fulfilment_attributes['last_name'] = name_last_name
        session.changed()

        raise HTTPFound(
            request.app.router['RegisterPersonSummary:get'].url_for(display_region=display_region,
                                                                    request_type=request_type))


@register_routes.view(r'/' + View.valid_display_regions + '/' + user_journey + '/' + valid_registration_types +
                      '/person-summary/')
class RegisterPersonSummary(View):
    @aiohttp_jinja2.template('register-person-summary.html')
    async def get(self, request):
        request_type = request.match_info['request_type']
        display_region = request.match_info['display_region']

        self.log_entry(request, display_region + '/' + user_journey + '/' + request_type + '/person-summary')

        session = await get_existing_session(request, user_journey, request_type)
        fulfilment_attributes = get_session_value(request, session, 'fulfilment_attributes', user_journey, request_type)

        page_title = 'Person summary'
        locale = 'en'

        return {
            'page_title': page_title,
            'display_region': display_region,
            'locale': locale,
            'request_type': request_type,
            'page_url': View.gen_page_url(request),
            'first_name': get_session_value(request, fulfilment_attributes, 'first_name', user_journey, request_type),
            'middle_names': get_session_value(request, fulfilment_attributes,
                                              'middle_names', user_journey, request_type),
            'last_name': get_session_value(request, fulfilment_attributes, 'last_name', user_journey, request_type)
        }

    async def post(self, request):
        display_region = request.match_info['display_region']
        request_type = request.match_info['request_type']
        self.log_entry(request, display_region + '/' + user_journey + '/' + request_type + '/person-summary')

        raise HTTPFound(
            request.app.router['RegisterConsent:get'].url_for(display_region=display_region,
                                                              request_type=request_type))
