import aiohttp_jinja2

from aiohttp.client_exceptions import (ClientResponseError)
from aiohttp.web import HTTPFound, RouteTableDef
from structlog import get_logger

from . import (ADDRESS_SELECT_CHECK_MSG,
               ADDRESS_SELECT_CHECK_MSG_CY,
               NO_SELECTION_CHECK_MSG,
               NO_SELECTION_CHECK_MSG_CY)

from .flash import flash
from .security import forget

from .exceptions import TooManyRequests, GetFulfilmentsError
from .security import invalidate

from .utils import View, FlashMessage
from .validators.address import AddressValidators
from .validators.identity import IdentityValidators
from .exceptions import InvalidDataError, InvalidDataErrorWelsh
from .session import get_existing_session, get_session_value
from .service_calls.rhsvc import RHSvc
from .service_calls.aims import Aims

logger = get_logger('respondent-home')
request_routes = RouteTableDef()

user_journey = 'request'
valid_request_types = r'{request_type:\baccess-code\b}'
valid_issue_types = r'{issue:\baddress-not-required|address-not-found\b}'


@request_routes.view(r'/' + View.valid_display_regions + '/' + user_journey + '/' + valid_request_types +
                     '/enter-address/')
class RequestEnterAddress(View):

    @aiohttp_jinja2.template('request-code-enter-address.html')
    async def get(self, request):
        display_region = request.match_info['display_region']
        request_type = request.match_info['request_type']

        self.log_entry(request, display_region + '/' + user_journey + '/' + request_type + '/enter-address')

        await forget(request)  # Removes identity in case user has existing auth session

        if display_region == 'cy':
            page_title = 'Enter address'
            if request.get('flash'):
                page_title = View.page_title_error_prefix_cy + page_title
            locale = 'cy'
        else:
            page_title = 'Enter address'
            if request.get('flash'):
                page_title = View.page_title_error_prefix_en + page_title
            locale = 'en'

        return {
            'display_region': display_region,
            'page_title': page_title,
            'user_journey': user_journey,
            'request_type': request_type,
            'locale': locale,
            'page_url': View.gen_page_url(request),
            'contact_us_link': View.get_campaign_site_link(request, display_region, 'contact-us'),
            'jwt': Aims.generate_jwt(request),
            'aims_domain': request.app['ADDRESS_INDEX_SVC_EXTERNAL_URL']
        }

    async def post(self, request):
        display_region = request.match_info['display_region']
        request_type = request.match_info['request_type']

        self.log_entry(request, display_region + '/' + user_journey + '/' + request_type + '/enter-address')

        session = await get_existing_session(request, user_journey, request_type)

        data = await request.post()

        if data.get('form-enter-address-postcode') or data.get('form-enter-address-postcode') == '':
            try:
                postcode = AddressValidators.validate_postcode(data['form-enter-address-postcode'], display_region)
                logger.info('valid postcode',
                            client_ip=request['client_ip'],
                            client_id=request['client_id'],
                            trace=request['trace'],
                            postcode_entered=postcode,
                            region_of_site=display_region)

            except (InvalidDataError, InvalidDataErrorWelsh) as exc:
                logger.info('invalid postcode',
                            client_ip=request['client_ip'], client_id=request['client_id'], trace=request['trace'])
                if exc.message_type == 'empty':
                    flash_message = FlashMessage.generate_flash_message(str(exc), 'ERROR', 'POSTCODE_ENTER_ERROR',
                                                                        'error_postcode_empty')
                else:
                    flash_message = FlashMessage.generate_flash_message(str(exc), 'ERROR', 'POSTCODE_ENTER_ERROR',
                                                                        'error_postcode_invalid')
                flash(request, flash_message)
                return HTTPFound(
                    request.app.router['RequestEnterAddress:get'].url_for(
                        display_region=display_region,
                        user_journey=user_journey,
                        request_type=request_type
                    ))

            fulfilment_attributes = {'postcode': postcode}
            session['fulfilment_attributes'] = fulfilment_attributes
            session.changed()

            return HTTPFound(
                request.app.router['RequestSelectAddress:get'].url_for(
                    display_region=display_region,
                    user_journey=user_journey,
                    request_type=request_type
                ))

        else:
            uprn = data['address-uprn']
            logger.info('UPRN of selected address: ' + data['address-uprn'])
            fulfilment_attributes = {'uprn': uprn}
            session['fulfilment_attributes'] = fulfilment_attributes
            session.changed()
            logger.info('session updated',
                        client_ip=request['client_ip'],
                        client_id=request['client_id'],
                        trace=request['trace'],
                        uprn_selected=uprn,
                        region_of_site=display_region)

            return HTTPFound(
                request.app.router['RequestConfirmAddress:get'].url_for(
                    display_region=display_region,
                    user_journey=user_journey,
                    request_type=request_type
                ))


@request_routes.view(r'/' + View.valid_display_regions + '/' + user_journey + '/' + valid_request_types +
                     '/select-address/')
class RequestSelectAddress(View):

    @aiohttp_jinja2.template('request-code-select-address.html')
    async def get(self, request):
        display_region = request.match_info['display_region']
        request_type = request.match_info['request_type']

        self.log_entry(request, display_region + '/' + user_journey + '/' + request_type + '/select-address')

        session = await get_existing_session(request, user_journey, request_type)

        if display_region == 'cy':
            page_title = 'Dewis cyfeiriad'
            if request.get('flash'):
                page_title = View.page_title_error_prefix_cy + page_title
            locale = 'cy'
        else:
            page_title = 'Select address'
            if request.get('flash'):
                page_title = View.page_title_error_prefix_en + page_title
            locale = 'en'

        fulfilment_attributes = get_session_value(request, session, 'fulfilment_attributes', user_journey, request_type)
        postcode = get_session_value(request, fulfilment_attributes, 'postcode', user_journey, request_type)

        address_content = await Aims.get_postcode_return(request, postcode, display_region)
        address_content['page_title'] = page_title
        address_content['display_region'] = display_region
        address_content['user_journey'] = user_journey
        address_content['request_type'] = request_type
        address_content['locale'] = locale
        address_content['page_url'] = View.gen_page_url(request)
        address_content['contact_us_link'] = View.get_campaign_site_link(request, display_region, 'contact-us')
        address_content['call_centre_number'] = View.get_contact_centre_number(display_region)

        return address_content

    async def post(self, request):
        display_region = request.match_info['display_region']
        request_type = request.match_info['request_type']

        self.log_entry(request, display_region + '/' + user_journey + '/' + request_type + '/select-address')

        session = await get_existing_session(request, user_journey, request_type)

        fulfilment_attributes = get_session_value(request, session, 'fulfilment_attributes', user_journey, request_type)

        data = await request.post()

        try:
            selected_uprn = data['form-pick-address']
        except KeyError:
            logger.info('no address selected',
                        client_ip=request['client_ip'],
                        client_id=request['client_id'],
                        trace=request['trace'],
                        region_of_site=display_region,
                        journey_requiring_address=user_journey)
            if display_region == 'cy':
                flash(request, ADDRESS_SELECT_CHECK_MSG_CY)
            else:
                flash(request, ADDRESS_SELECT_CHECK_MSG)
            return HTTPFound(
                request.app.router['RequestSelectAddress:get'].url_for(
                    display_region=display_region,
                    user_journey=user_journey,
                    request_type=request_type
                ))

        if selected_uprn == 'xxxx':
            return HTTPFound(
                request.app.router['RequestContactCentre:get'].url_for(
                    display_region=display_region,
                    user_journey=user_journey,
                    request_type=request_type,
                    issue='address-not-found'
                ))
        else:
            fulfilment_attributes['uprn'] = selected_uprn
            session.changed()
            logger.info('session updated',
                        client_ip=request['client_ip'],
                        client_id=request['client_id'],
                        trace=request['trace'],
                        uprn_selected=selected_uprn,
                        region_of_site=display_region)

        return HTTPFound(
            request.app.router['RequestConfirmAddress:get'].url_for(
                display_region=display_region,
                user_journey=user_journey,
                request_type=request_type
            ))


@request_routes.view(r'/' + View.valid_display_regions + '/' + user_journey + '/' + valid_request_types +
                     '/confirm-address/')
class RequestConfirmAddress(View):
    @aiohttp_jinja2.template('request-code-confirm-address.html')
    async def get(self, request):
        display_region = request.match_info['display_region']
        request_type = request.match_info['request_type']

        self.log_entry(request, display_region + '/' + user_journey + '/' + request_type + '/confirm-address')

        session = await get_existing_session(request, user_journey, request_type)

        if display_region == 'cy':
            page_title = 'Cadarnhau cyfeiriad'
            if request.get('flash'):
                page_title = View.page_title_error_prefix_cy + page_title
            locale = 'cy'
        else:
            page_title = 'Confirm address'
            if request.get('flash'):
                page_title = View.page_title_error_prefix_en + page_title
            locale = 'en'

        fulfilment_attributes = get_session_value(request, session, 'fulfilment_attributes', user_journey, request_type)
        uprn = get_session_value(request, fulfilment_attributes, 'uprn', user_journey, request_type)

        try:
            rhsvc_uprn_return = await RHSvc.get_cases_by_uprn(request, uprn)
            logger.info('case matching uprn found in RHSvc',
                        client_ip=request['client_ip'],
                        client_id=request['client_id'],
                        trace=request['trace'])
            fulfilment_attributes['addressLine1'] = rhsvc_uprn_return['address']['addressLine1']
            fulfilment_attributes['addressLine2'] = rhsvc_uprn_return['address']['addressLine2']
            fulfilment_attributes['addressLine3'] = rhsvc_uprn_return['address']['addressLine3']
            fulfilment_attributes['townName'] = rhsvc_uprn_return['address']['townName']
            fulfilment_attributes['postcode'] = rhsvc_uprn_return['address']['postcode']
            fulfilment_attributes['uprn'] = rhsvc_uprn_return['address']['uprn']
            fulfilment_attributes['case_id'] = rhsvc_uprn_return['caseId']
            fulfilment_attributes['region'] = rhsvc_uprn_return['address']['region']
            fulfilment_attributes['survey_id'] = rhsvc_uprn_return['surveyId']

            session.changed()

        except ClientResponseError as ex:
            if ex.status == 404:
                logger.info('no case matching uprn in RHSvc - using AIMS data',
                            client_ip=request['client_ip'],
                            client_id=request['client_id'],
                            trace=request['trace'])

                aims_uprn_return = await Aims.get_ai_uprn(request, uprn)

                # Ensure no session data from previous RM case used later
                if 'case_id' in fulfilment_attributes:
                    del fulfilment_attributes['case_id']
                    session.changed()
                fulfilment_attributes['addressLine1'] = aims_uprn_return['response']['address']['addressLine1']
                fulfilment_attributes['addressLine2'] = aims_uprn_return['response']['address']['addressLine2']
                fulfilment_attributes['addressLine3'] = aims_uprn_return['response']['address']['addressLine3']
                fulfilment_attributes['townName'] = aims_uprn_return['response']['address']['townName']
                fulfilment_attributes['postcode'] = aims_uprn_return['response']['address']['postcode']
                fulfilment_attributes['uprn'] = aims_uprn_return['response']['address']['uprn']
                fulfilment_attributes['region'] = aims_uprn_return['response']['address']['countryCode']
            else:
                logger.info('error response from RHSvc',
                            client_ip=request['client_ip'],
                            client_id=request['client_id'],
                            trace=request['trace'],
                            status_code=ex.status)
                raise ex

        return {
            'page_title': page_title,
            'display_region': display_region,
            'user_journey': user_journey,
            'request_type': request_type,
            'locale': locale,
            'page_url': View.gen_page_url(request),
            'addressLine1': get_session_value(request, fulfilment_attributes, 'addressLine1',
                                              user_journey, request_type),
            'addressLine2': get_session_value(request, fulfilment_attributes, 'addressLine2',
                                              user_journey, request_type),
            'addressLine3': get_session_value(request, fulfilment_attributes, 'addressLine3',
                                              user_journey, request_type),
            'townName': get_session_value(request, fulfilment_attributes, 'townName', user_journey, request_type),
            'postcode': get_session_value(request, fulfilment_attributes, 'postcode', user_journey, request_type)
        }

    async def post(self, request):
        tracking = {"client_ip": request['client_ip'], "client_id": request['client_id'], "trace": request['trace']}

        display_region = request.match_info['display_region']
        request_type = request.match_info['request_type']

        self.log_entry(request, display_region + '/' + user_journey + '/' + request_type + '/confirm-address')

        session = await get_existing_session(request, user_journey, request_type)
        fulfilment_attributes = get_session_value(request, session, 'fulfilment_attributes', user_journey, request_type)
        data = await request.post()

        try:
            address_confirmation = data['form-confirm-address']
        except KeyError:
            logger.info('address confirmation error', **tracking, region_of_site=display_region)
            if display_region == 'cy':
                flash(request, NO_SELECTION_CHECK_MSG_CY)
            else:
                flash(request, NO_SELECTION_CHECK_MSG)
            return HTTPFound(
                request.app.router['RequestConfirmAddress:get'].url_for(
                    display_region=display_region,
                    user_journey=user_journey,
                    request_type=request_type
                ))

        if address_confirmation == 'yes':
            if 'case_id' in fulfilment_attributes:
                return HTTPFound(
                    request.app.router['RequestCodeSelectHowToReceive:get'].url_for(
                        request_type=request_type, display_region=display_region))
            else:
                logger.info('no case matching uprn in RHSvc - return customer contact centre page',
                            client_ip=request['client_ip'],
                            client_id=request['client_id'],
                            trace=request['trace'])
                return HTTPFound(
                    request.app.router['RequestContactCentre:get'].url_for(
                        display_region=display_region,
                        user_journey=user_journey,
                        request_type=request_type,
                        issue='address-not-required'
                    ))

        elif address_confirmation == 'no':
            return HTTPFound(
                request.app.router['RequestEnterAddress:get'].url_for(display_region=display_region,
                                                                      user_journey=user_journey,
                                                                      request_type=request_type))

        else:
            # catch all just in case, should never get here
            logger.info('address confirmation error', **tracking, user_selection=address_confirmation)
            if display_region == 'cy':
                flash(request, NO_SELECTION_CHECK_MSG_CY)
            else:
                flash(request, NO_SELECTION_CHECK_MSG)
            return HTTPFound(
                request.app.router['RequestConfirmAddress:get'].url_for(
                    display_region=display_region,
                    user_journey=user_journey,
                    request_type=request_type
                ))


@request_routes.view(r'/' + View.valid_display_regions + '/' + user_journey + '/' + valid_request_types +
                     '/select-how-to-receive/')
class RequestCodeSelectHowToReceive(View):
    @aiohttp_jinja2.template('request-code-select-how-to-receive.html')
    async def get(self, request):

        request_type = request.match_info['request_type']
        display_region = request.match_info['display_region']

        self.log_entry(request, display_region + '/request/' + request_type + '/select-how-to-receive')

        session = await get_existing_session(request, user_journey, request_type)
        fulfilment_attributes = get_session_value(request, session, 'fulfilment_attributes', user_journey, request_type)

        if display_region == 'cy':
            page_title = 'Select how to receive access code'
            if request.get('flash'):
                page_title = View.page_title_error_prefix_cy + page_title
            label_text_sms = 'Neges destun'
            label_description_sms = 'We will need your mobile number for this'
            label_text_print = 'Post'
            label_description_print = "Dim ond i'r cyfeiriad cofrestredig y gallwn anfon codau mynediad"
            label_text_email = 'Email'
            label_description_email = 'We will need your email address for this'
            locale = 'cy'
        else:
            page_title = 'Select how to receive access code'
            if request.get('flash'):
                page_title = View.page_title_error_prefix_en + page_title
            label_text_sms = 'Text message'
            label_description_sms = 'We will need your mobile number for this'
            label_text_print = 'Post'
            label_description_print = 'We can only send access codes to the registered address'
            label_text_email = 'Email'
            label_description_email = 'We will need your email address for this'
            locale = 'en'

        survey_id = get_session_value(request, fulfilment_attributes, 'survey_id', user_journey, request_type)
        survey_data = await RHSvc.get_survey_details(request, survey_id)

        form_option_set = []

        if survey_data.get('allowedSmsFulfilments'):
            form_option_set.append({
                'id': 'sms',
                'label': {
                    'text': label_text_sms,
                    'description': label_description_sms
                },
                'value': 'sms'
            })
        if survey_data.get('allowedPrintFulfilments'):
            form_option_set.append({
                'id': 'post',
                'label': {
                    'text': label_text_print,
                    'description': label_description_print
                },
                'value': 'post'
            })
        if survey_data.get('allowedEmailFulfilments'):
            form_option_set.append({
                'id': 'email',
                'label': {
                    'text': label_text_email,
                    'description': label_description_email
                },
                'value': 'email'
            })

        if (not survey_data.get('allowedSmsFulfilments')) and \
                (not survey_data.get('allowedPrintFulfilments')) and \
                (not survey_data.get('allowedEmailFulfilments')):
            logger.info('no valid fulfilments available',
                        client_ip=request['client_ip'],
                        client_id=request['client_id'],
                        trace=request['trace'])
            raise GetFulfilmentsError

        return {
            'page_title': page_title,
            'display_region': display_region,
            'locale': locale,
            'request_type': request_type,
            'page_url': View.gen_page_url(request),
            'contact_us_link': View.get_campaign_site_link(request, display_region, 'contact-us'),
            'form_option_set': form_option_set
        }

    async def post(self, request):

        request_type = request.match_info['request_type']
        display_region = request.match_info['display_region']

        await get_existing_session(request, user_journey, request_type)

        self.log_entry(request, display_region + '/request/' + request_type + '/select-how-to-receive')

        data = await request.post()
        try:
            request_method = data['form-select-method']
        except KeyError:
            logger.info('request method selection error',
                        client_ip=request['client_ip'], client_id=request['client_id'], trace=request['trace'])
            if display_region == 'cy':
                flash(request, NO_SELECTION_CHECK_MSG_CY)
            else:
                flash(request, NO_SELECTION_CHECK_MSG)
            return HTTPFound(
                request.app.router['RequestCodeSelectHowToReceive:get'].url_for(
                    display_region=display_region,
                    request_type=request_type
                ))

        if request_method == 'sms':
            return HTTPFound(
                request.app.router['RequestCodeEnterMobile:get'].url_for(request_type=request_type,
                                                                         display_region=display_region))
        elif request_method == 'post':
            return HTTPFound(
                request.app.router['RequestCommonEnterName:get'].url_for(request_type=request_type,
                                                                         display_region=display_region))
        elif request_method == 'email':
            return HTTPFound(
                request.app.router['RequestCodeEnterEmail:get'].url_for(request_type=request_type,
                                                                        display_region=display_region))

        else:
            # catch all just in case, should never get here
            logger.info('request method selection error',
                        client_ip=request['client_ip'],
                        client_id=request['client_id'],
                        trace=request['trace'],
                        method_selected=request_method)
            if display_region == 'cy':
                flash(request, NO_SELECTION_CHECK_MSG_CY)
            else:
                flash(request, NO_SELECTION_CHECK_MSG)
            return HTTPFound(
                request.app.router['RequestCodeSelectHowToReceive:get'].url_for(
                    display_region=display_region,
                    request_type=request_type
                ))


@request_routes.view(r'/' + View.valid_display_regions + '/' + user_journey + '/' + valid_request_types +
                     '/enter-mobile/')
class RequestCodeEnterMobile(View):
    @aiohttp_jinja2.template('request-code-enter-mobile.html')
    async def get(self, request):
        request_type = request.match_info['request_type']
        display_region = request.match_info['display_region']

        if display_region == 'cy':
            page_title = 'Nodi rhif ffôn symudol'
            if request.get('flash'):
                page_title = View.page_title_error_prefix_cy + page_title
            locale = 'cy'
        else:
            page_title = 'Enter mobile number'
            if request.get('flash'):
                page_title = View.page_title_error_prefix_en + page_title
            locale = 'en'

        self.log_entry(request, display_region + '/request/' + request_type + '/enter-mobile')

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

        if display_region == 'cy':
            locale = 'cy'
        else:
            locale = 'en'

        self.log_entry(request, display_region + '/request/' + request_type + '/enter-mobile')

        session = await get_existing_session(request, user_journey, request_type)
        fulfilment_attributes = get_session_value(request, session, 'fulfilment_attributes', user_journey, request_type)

        data = await request.post()

        try:
            mobile_number = IdentityValidators.validate_uk_mobile_phone_number(data['request-mobile-number'], locale)

            logger.info('valid mobile number',
                        client_ip=request['client_ip'], client_id=request['client_id'], trace=request['trace'])

            fulfilment_attributes['mobile_number'] = mobile_number
            fulfilment_attributes['submitted_mobile_number'] = data['request-mobile-number']
            session.changed()

            return HTTPFound(
                request.app.router['RequestCodeConfirmSendByText:get'].url_for(request_type=request_type,
                                                                               display_region=display_region))

        except (InvalidDataError, InvalidDataErrorWelsh) as exc:
            logger.info(exc, client_ip=request['client_ip'], client_id=request['client_id'], trace=request['trace'])
            if exc.message_type == 'empty':
                flash_message = FlashMessage.generate_flash_message(str(exc), 'ERROR', 'MOBILE_ENTER_ERROR',
                                                                    'mobile_empty')
            else:
                flash_message = FlashMessage.generate_flash_message(str(exc), 'ERROR', 'MOBILE_ENTER_ERROR',
                                                                    'mobile_invalid')
            flash(request, flash_message)
            return HTTPFound(
                request.app.router['RequestCodeEnterMobile:get'].url_for(
                    display_region=display_region,
                    request_type=request_type
                ))


@request_routes.view(r'/' + View.valid_display_regions + '/' + user_journey + '/' + valid_request_types +
                     '/confirm-send-by-text/')
class RequestCodeConfirmSendByText(View):
    @aiohttp_jinja2.template('request-code-confirm-send-by-text.html')
    async def get(self, request):

        request_type = request.match_info['request_type']
        display_region = request.match_info['display_region']

        self.log_entry(request, display_region + '/' + user_journey + '/' + request_type + '/confirm-send-by-text')

        session = await get_existing_session(request, user_journey, request_type)
        fulfilment_attributes = get_session_value(request, session, 'fulfilment_attributes', user_journey, request_type)

        if display_region == 'cy':
            page_title = 'Confirm to send access code by text'
            if request.get('flash'):
                page_title = View.page_title_error_prefix_cy + page_title
            locale = 'cy'
        else:
            page_title = 'Confirm to send access code by text'
            if request.get('flash'):
                page_title = View.page_title_error_prefix_en + page_title
            locale = 'en'

        return {
            'page_title': page_title,
            'display_region': display_region,
            'locale': locale,
            'request_type': request_type,
            'page_url': View.gen_page_url(request),
            'submitted_mobile_number': get_session_value(request, fulfilment_attributes,
                                                         'submitted_mobile_number', user_journey)
        }

    async def post(self, request):

        request_type = request.match_info['request_type']
        display_region = request.match_info['display_region']

        self.log_entry(request, display_region + '/request/' + request_type + '/confirm-send-by-text')

        session = await get_existing_session(request, user_journey, request_type)
        fulfilment_attributes = get_session_value(request, session, 'fulfilment_attributes', user_journey, request_type)

        data = await request.post()
        try:
            mobile_confirmation = data['request-mobile-confirmation']
        except KeyError:
            logger.info('mobile confirmation error',
                        client_ip=request['client_ip'], client_id=request['client_id'], trace=request['trace'])
            if display_region == 'cy':
                flash(request, NO_SELECTION_CHECK_MSG_CY)
            else:
                flash(request, NO_SELECTION_CHECK_MSG)
            return HTTPFound(
                request.app.router['RequestCodeConfirmSendByText:get'].url_for(
                    display_region=display_region,
                    request_type=request_type
                ))

        if mobile_confirmation == 'yes':
            region = get_session_value(request, fulfilment_attributes, 'region', user_journey, request_type)
            postcode = get_session_value(request, fulfilment_attributes, 'postcode', user_journey, request_type)
            case_id = get_session_value(request, fulfilment_attributes, 'case_id', user_journey, request_type)
            survey_id = get_session_value(request, fulfilment_attributes, 'survey_id', user_journey, request_type)
            mobile_number = get_session_value(request, fulfilment_attributes,
                                              'mobile_number', user_journey, request_type)

            fulfilment_individual = 'false'

            if display_region == 'cy':
                fulfilment_language = 'W'
            else:
                fulfilment_language = 'E'

            logger.info(f"fulfilment query: region={region}, "
                        f"individual={fulfilment_individual}",
                        client_ip=request['client_ip'],
                        client_id=request['client_id'],
                        trace=request['trace'],
                        postcode=postcode)

            fulfilment_code_array = []

            try:
                available_fulfilments = \
                    await RHSvc.survey_fulfilments_by_type(request, 'sms', survey_id, fulfilment_language)

                fulfilment_code_array.append(available_fulfilments)

                try:
                    await RHSvc.request_fulfilment_sms(request,
                                                                  case_id,
                                                                  mobile_number,
                                                                  fulfilment_code_array)
                except (KeyError, ClientResponseError) as ex:
                    if ex.status == 429:
                        raise TooManyRequests(request_type)
                    else:
                        raise ex

                return HTTPFound(
                    request.app.router['RequestCodeSentByText:get'].url_for(request_type=request_type,
                                                                            display_region=display_region))
            except ClientResponseError as ex:
                raise ex

        elif mobile_confirmation == 'no':
            return HTTPFound(
                request.app.router['RequestCodeEnterMobile:get'].url_for(request_type=request_type,
                                                                         display_region=display_region))

        else:
            # catch all just in case, should never get here
            logger.info('mobile confirmation error',
                        client_ip=request['client_ip'],
                        client_id=request['client_id'],
                        trace=request['trace'],
                        user_selection=mobile_confirmation)
            if display_region == 'cy':
                flash(request, NO_SELECTION_CHECK_MSG_CY)
            else:
                flash(request, NO_SELECTION_CHECK_MSG)
            return HTTPFound(
                request.app.router['RequestCodeConfirmSendByText:get'].url_for(
                    display_region=display_region,
                    request_type=request_type
                ))


@request_routes.view(r'/' + View.valid_display_regions + '/' + user_journey + '/' + valid_request_types +
                     '/enter-email/')
class RequestCodeEnterEmail(View):
    @aiohttp_jinja2.template('request-code-enter-email.html')
    async def get(self, request):
        request_type = request.match_info['request_type']
        display_region = request.match_info['display_region']

        if display_region == 'cy':
            page_title = 'Enter email address'
            if request.get('flash'):
                page_title = View.page_title_error_prefix_cy + page_title
            locale = 'cy'
        else:
            page_title = 'Enter email address'
            if request.get('flash'):
                page_title = View.page_title_error_prefix_en + page_title
            locale = 'en'

        self.log_entry(request, display_region + '/request/' + request_type + '/enter-email')

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

        if display_region == 'cy':
            locale = 'cy'
        else:
            locale = 'en'

        self.log_entry(request, display_region + '/request/' + request_type + '/enter-email')

        session = await get_existing_session(request, user_journey, request_type)
        fulfilment_attributes = get_session_value(request, session, 'fulfilment_attributes', user_journey, request_type)

        data = await request.post()

        try:
            email = IdentityValidators.validate_email(data['request-email'], locale)

            logger.info('valid email address',
                        client_ip=request['client_ip'], client_id=request['client_id'], trace=request['trace'])

            fulfilment_attributes['email'] = email
            session.changed()

            return HTTPFound(
                request.app.router['RequestCodeConfirmSendByEmail:get'].url_for(request_type=request_type,
                                                                                display_region=display_region))

        except (InvalidDataError, InvalidDataErrorWelsh) as exc:
            logger.info(exc, client_ip=request['client_ip'], client_id=request['client_id'], trace=request['trace'])
            if exc.message_type == 'empty':
                flash_message = FlashMessage.generate_flash_message(str(exc), 'ERROR', 'EMAIL_ENTER_ERROR',
                                                                    'email_empty')
            else:
                flash_message = FlashMessage.generate_flash_message(str(exc), 'ERROR', 'EMAIL_ENTER_ERROR',
                                                                    'email_invalid')
            flash(request, flash_message)
            return HTTPFound(
                request.app.router['RequestCodeEnterEmail:get'].url_for(
                    display_region=display_region,
                    request_type=request_type
                ))


@request_routes.view(r'/' + View.valid_display_regions + '/' + user_journey + '/' + valid_request_types +
                     '/confirm-send-by-email/')
class RequestCodeConfirmSendByEmail(View):
    @aiohttp_jinja2.template('request-code-confirm-send-by-email.html')
    async def get(self, request):

        request_type = request.match_info['request_type']
        display_region = request.match_info['display_region']

        self.log_entry(request, display_region + '/' + user_journey + '/' + request_type + '/confirm-send-by-email')

        session = await get_existing_session(request, user_journey, request_type)
        fulfilment_attributes = get_session_value(request, session, 'fulfilment_attributes', user_journey, request_type)

        if display_region == 'cy':
            page_title = 'Confirm to send access code by email'
            if request.get('flash'):
                page_title = View.page_title_error_prefix_cy + page_title
            locale = 'cy'
        else:
            page_title = 'Confirm to send access code by email'
            if request.get('flash'):
                page_title = View.page_title_error_prefix_en + page_title
            locale = 'en'

        return {
            'page_title': page_title,
            'display_region': display_region,
            'locale': locale,
            'request_type': request_type,
            'page_url': View.gen_page_url(request),
            'email': get_session_value(request, fulfilment_attributes, 'email', user_journey)
        }

    async def post(self, request):

        request_type = request.match_info['request_type']
        display_region = request.match_info['display_region']

        self.log_entry(request, display_region + '/request/' + request_type + '/confirm-send-by-email')

        session = await get_existing_session(request, user_journey, request_type)
        fulfilment_attributes = get_session_value(request, session, 'fulfilment_attributes', user_journey, request_type)

        data = await request.post()
        try:
            email_confirmation = data['request-email-confirmation']
        except KeyError:
            logger.info('email confirmation error',
                        client_ip=request['client_ip'], client_id=request['client_id'], trace=request['trace'])
            if display_region == 'cy':
                flash(request, NO_SELECTION_CHECK_MSG_CY)
            else:
                flash(request, NO_SELECTION_CHECK_MSG)
            return HTTPFound(
                request.app.router['RequestCodeConfirmSendByEmail:get'].url_for(
                    display_region=display_region,
                    request_type=request_type
                ))

        if email_confirmation == 'yes':
            region = get_session_value(request, fulfilment_attributes, 'region', user_journey, request_type)
            postcode = get_session_value(request, fulfilment_attributes, 'postcode', user_journey, request_type)
            case_id = get_session_value(request, fulfilment_attributes, 'case_id', user_journey, request_type)
            survey_id = get_session_value(request, fulfilment_attributes, 'survey_id', user_journey, request_type)
            email = get_session_value(request, fulfilment_attributes, 'email', user_journey, request_type)

            fulfilment_individual = 'false'

            if display_region == 'cy':
                fulfilment_language = 'W'
            else:
                fulfilment_language = 'E'

            logger.info(f"fulfilment query: region={region}, "
                        f"individual={fulfilment_individual}",
                        client_ip=request['client_ip'],
                        client_id=request['client_id'],
                        trace=request['trace'],
                        postcode=postcode)

            fulfilment_code_array = []

            try:
                available_fulfilments = \
                    await RHSvc.survey_fulfilments_by_type(request, 'email', survey_id, fulfilment_language)

                fulfilment_code_array.append(available_fulfilments)

                try:
                    await RHSvc.request_fulfilment_email(request,
                                                                    case_id,
                                                                    email,
                                                                    fulfilment_code_array)
                except (KeyError, ClientResponseError) as ex:
                    if ex.status == 429:
                        raise TooManyRequests(request_type)
                    else:
                        raise ex

                return HTTPFound(
                    request.app.router['RequestCodeSentByEmail:get'].url_for(request_type=request_type,
                                                                             display_region=display_region))
            except ClientResponseError as ex:
                raise ex

        elif email_confirmation == 'no':
            return HTTPFound(
                request.app.router['RequestCodeEnterEmail:get'].url_for(request_type=request_type,
                                                                        display_region=display_region))

        else:
            # catch all just in case, should never get here
            logger.info('email confirmation error',
                        client_ip=request['client_ip'],
                        client_id=request['client_id'],
                        trace=request['trace'],
                        user_selection=email_confirmation)
            if display_region == 'cy':
                flash(request, NO_SELECTION_CHECK_MSG_CY)
            else:
                flash(request, NO_SELECTION_CHECK_MSG)
            return HTTPFound(
                request.app.router['RequestCodeConfirmSendByEmail:get'].url_for(
                    display_region=display_region,
                    request_type=request_type
                ))


@request_routes.view(r'/' + View.valid_display_regions + '/' + user_journey + '/' + valid_request_types +
                     '/enter-name/')
class RequestCommonEnterName(View):
    @aiohttp_jinja2.template('request-code-enter-name.html')
    async def get(self, request):

        request_type = request.match_info['request_type']
        display_region = request.match_info['display_region']

        if display_region == 'cy':
            page_title = "Nodi enw"
            if request.get('flash'):
                page_title = View.page_title_error_prefix_cy + page_title
            locale = 'cy'
        else:
            page_title = "Enter name"
            if request.get('flash'):
                page_title = View.page_title_error_prefix_en + page_title
            locale = 'en'

        self.log_entry(request, display_region + '/request/' + request_type + '/enter-name')

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

        self.log_entry(request, display_region + '/request/' + request_type + '/enter-name')

        session = await get_existing_session(request, user_journey, request_type)
        fulfilment_attributes = get_session_value(request, session, 'fulfilment_attributes', user_journey, request_type)

        data = await request.post()

        form_valid = IdentityValidators.validate_name(request, data, display_region)

        if not form_valid:
            logger.info('form submission error',
                        client_ip=request['client_ip'],
                        client_id=request['client_id'],
                        trace=request['trace'],
                        region_of_site=display_region,
                        type_of_request=request_type)
            return HTTPFound(
                request.app.router['RequestCommonEnterName:get'].url_for(
                    display_region=display_region,
                    request_type=request_type
                ))

        name_first_name = data['name_first_name'].strip()
        name_last_name = data['name_last_name'].strip()

        fulfilment_attributes['first_name'] = name_first_name
        fulfilment_attributes['last_name'] = name_last_name
        session.changed()

        return HTTPFound(
            request.app.router['RequestCommonConfirmSendByPost:get'].url_for(display_region=display_region,
                                                                             request_type=request_type))


@request_routes.view(r'/' + View.valid_display_regions + '/' + user_journey + '/' + valid_request_types +
                     '/confirm-send-by-post/')
class RequestCommonConfirmSendByPost(View):
    @aiohttp_jinja2.template('request-code-confirm-send-by-post.html')
    async def get(self, request):
        request_type = request.match_info['request_type']
        display_region = request.match_info['display_region']

        if display_region == 'cy':
            locale = 'cy'
        else:
            locale = 'en'

        self.log_entry(request, display_region + '/request/' + request_type + '/confirm-send-by-post')

        session = await get_existing_session(request, user_journey, request_type)
        fulfilment_attributes = get_session_value(request, session, 'fulfilment_attributes', user_journey, request_type)

        if display_region == 'cy':
            page_title = "Confirm to send access code by post"
        else:
            page_title = 'Confirm to send access code by post'

        if request.get('flash'):
            if display_region == 'cy':
                page_title = View.page_title_error_prefix_cy + page_title
            else:
                page_title = View.page_title_error_prefix_en + page_title

        return {
            'page_title': page_title,
            'display_region': display_region,
            'locale': locale,
            'request_type': request_type,
            'page_url': View.gen_page_url(request),
            'first_name': get_session_value(request, fulfilment_attributes, 'first_name', user_journey, request_type),
            'last_name': get_session_value(request, fulfilment_attributes, 'last_name', user_journey, request_type),
            'addressLine1': get_session_value(request, fulfilment_attributes, 'addressLine1',
                                              user_journey, request_type),
            'addressLine2': get_session_value(request, fulfilment_attributes, 'addressLine2',
                                              user_journey, request_type),
            'addressLine3': get_session_value(request, fulfilment_attributes, 'addressLine3',
                                              user_journey, request_type),
            'townName': get_session_value(request, fulfilment_attributes, 'townName', user_journey, request_type),
            'postcode': get_session_value(request, fulfilment_attributes, 'postcode', user_journey, request_type)
        }

    async def post(self, request):
        request_type = request.match_info['request_type']
        display_region = request.match_info['display_region']

        self.log_entry(request, display_region + '/' + user_journey + '/' + request_type + '/confirm-send-by-post')

        session = await get_existing_session(request, user_journey, request_type)
        fulfilment_attributes = get_session_value(request, session, 'fulfilment_attributes', user_journey, request_type)

        data = await request.post()
        try:
            name_address_confirmation = data['request-name-address-confirmation']
        except KeyError:
            logger.info('name confirmation error',
                        client_ip=request['client_ip'],
                        client_id=request['client_id'],
                        trace=request['trace'],
                        type_of_request=request_type,
                        region_of_site=display_region)
            if display_region == 'cy':
                flash(request, NO_SELECTION_CHECK_MSG_CY)
            else:
                flash(request, NO_SELECTION_CHECK_MSG)

            return HTTPFound(
                request.app.router['RequestCommonConfirmSendByPost:get'].url_for(display_region=display_region,
                                                                                 request_type=request_type))

        if name_address_confirmation == 'yes':
            region = get_session_value(request, fulfilment_attributes, 'region', user_journey, request_type)
            first_name = get_session_value(request, fulfilment_attributes, 'first_name', user_journey, request_type)
            last_name = get_session_value(request, fulfilment_attributes, 'last_name', user_journey, request_type)
            case_id = get_session_value(request, fulfilment_attributes, 'case_id', user_journey, request_type)
            survey_id = get_session_value(request, fulfilment_attributes, 'survey_id', user_journey, request_type)
            postcode = get_session_value(request, fulfilment_attributes, 'postcode', user_journey, request_type)

            fulfilment_individual = 'false'

            if display_region == 'cy':
                fulfilment_language = 'W'
            else:
                fulfilment_language = 'E'

            fulfilment_code_array = []

            try:
                available_fulfilments = \
                    await RHSvc.survey_fulfilments_by_type(request, 'post', survey_id, fulfilment_language)

                fulfilment_code_array.append(available_fulfilments)

                logger.info(
                    f"fulfilment query: region={region}, individual={fulfilment_individual}",
                    client_ip=request['client_ip'],
                    client_id=request['client_id'],
                    trace=request['trace'],
                    postcode=postcode)

                try:
                    await RHSvc.request_fulfilment_post(request,
                                                                   case_id,
                                                                   first_name,
                                                                   last_name,
                                                                   fulfilment_code_array,
                                                                   None)
                except (KeyError, ClientResponseError) as ex:
                    if ex.status == 429:
                        raise TooManyRequests(request_type)
                    else:
                        raise ex

                return HTTPFound(
                    request.app.router['RequestCodeSentByPost:get'].url_for(display_region=display_region,
                                                                            request_type=request_type))

            except ClientResponseError as ex:
                raise ex

        elif name_address_confirmation == 'no':
            return HTTPFound(
                request.app.router['RequestCodeEnterMobile:get'].url_for(display_region=display_region,
                                                                         request_type=request_type))

        else:
            # catch all just in case, should never get here
            logger.info('name confirmation error',
                        client_ip=request['client_ip'],
                        client_id=request['client_id'],
                        trace=request['trace'],
                        user_selection=name_address_confirmation,
                        region_of_site=display_region,
                        type_of_request=request_type)
            if display_region == 'cy':
                flash(request, NO_SELECTION_CHECK_MSG_CY)
            else:
                flash(request, NO_SELECTION_CHECK_MSG)

            return HTTPFound(
                request.app.router['RequestCommonConfirmSendByPost:get'].url_for(display_region=display_region,
                                                                                 request_type=request_type))


@request_routes.view(r'/' + View.valid_display_regions + '/' + user_journey + '/' + valid_request_types +
                     '/code-sent-by-text/')
class RequestCodeSentByText(View):
    @aiohttp_jinja2.template('request-code-sent-by-text.html')
    async def get(self, request):

        request_type = request.match_info['request_type']
        display_region = request.match_info['display_region']

        self.log_entry(request, display_region + '/request/' + request_type + '/code-sent-by-text')

        session = await get_existing_session(request, user_journey, request_type)
        fulfilment_attributes = get_session_value(request, session, 'fulfilment_attributes', user_journey, request_type)

        if display_region == 'cy':
            page_title = "Access code has been sent by text"
            locale = 'cy'
        else:
            page_title = 'Access code has been sent by text'
            locale = 'en'

        await invalidate(request)

        return {
            'page_title': page_title,
            'display_region': display_region,
            'locale': locale,
            'request_type': request_type,
            'page_url': View.gen_page_url(request),
            'submitted_mobile_number': get_session_value(request, fulfilment_attributes,
                                                         'submitted_mobile_number', user_journey)
        }


@request_routes.view(r'/' + View.valid_display_regions + '/' + user_journey + '/' + valid_request_types +
                     '/code-sent-by-email/')
class RequestCodeSentByEmail(View):
    @aiohttp_jinja2.template('request-code-sent-by-email.html')
    async def get(self, request):

        request_type = request.match_info['request_type']
        display_region = request.match_info['display_region']

        self.log_entry(request, display_region + '/request/' + request_type + '/code-sent-by-email')

        session = await get_existing_session(request, user_journey, request_type)
        fulfilment_attributes = get_session_value(request, session, 'fulfilment_attributes', user_journey, request_type)

        if display_region == 'cy':
            page_title = "Access code has been sent by email"
            locale = 'cy'
        else:
            page_title = 'Access code has been sent by email'
            locale = 'en'

        await invalidate(request)

        return {
            'page_title': page_title,
            'display_region': display_region,
            'locale': locale,
            'request_type': request_type,
            'page_url': View.gen_page_url(request),
            'email': get_session_value(request, fulfilment_attributes, 'email', user_journey)
        }


@request_routes.view(r'/' + View.valid_display_regions + '/' + user_journey + '/' + valid_request_types +
                     '/code-sent-by-post/')
class RequestCodeSentByPost(View):
    @aiohttp_jinja2.template('request-code-sent-by-post.html')
    async def get(self, request):

        request_type = request.match_info['request_type']
        display_region = request.match_info['display_region']

        self.log_entry(request, display_region + '/' + user_journey + '/' + request_type + '/code-sent-by-post')

        session = await get_existing_session(request, user_journey, request_type)
        fulfilment_attributes = get_session_value(request, session, 'fulfilment_attributes', user_journey, request_type)

        if display_region == 'cy':
            page_title = "Access code will be sent by post"
            locale = 'cy'
        else:
            page_title = 'Access code will be sent by post'
            locale = 'en'

        await invalidate(request)

        return {
                'page_title': page_title,
                'display_region': display_region,
                'locale': locale,
                'request_type': request_type,
                'page_url': View.gen_page_url(request),
                'home_link': View.get_campaign_site_link(request, display_region, 'surveys-home'),
                'first_name': get_session_value(request, fulfilment_attributes, 'first_name',
                                                user_journey, request_type),
                'last_name': get_session_value(request, fulfilment_attributes, 'last_name', user_journey, request_type),
                'addressLine1': get_session_value(request, fulfilment_attributes, 'addressLine1',
                                                  user_journey, request_type),
                'addressLine2': get_session_value(request, fulfilment_attributes, 'addressLine2',
                                                  user_journey, request_type),
                'addressLine3': get_session_value(request, fulfilment_attributes, 'addressLine3',
                                                  user_journey, request_type),
                'townName': get_session_value(request, fulfilment_attributes, 'townName', user_journey, request_type),
                'postcode': get_session_value(request, fulfilment_attributes, 'postcode', user_journey, request_type)
            }


@request_routes.view(r'/' + View.valid_display_regions + '/' + user_journey + '/' + valid_request_types + '/' +
                     valid_issue_types + '/')
class RequestContactCentre(View):
    @aiohttp_jinja2.template('request-contact-centre.html')
    async def get(self, request):
        display_region = request.match_info['display_region']
        request_type = request.match_info['request_type']
        issue = request.match_info['issue']

        if display_region == 'cy':
            page_title = "Customer Contact Centre"
            locale = 'cy'
        else:
            page_title = 'Customer Contact Centre'
            locale = 'en'

        self.log_entry(request, display_region + '/' + user_journey + '/' + request_type + '/' + issue)

        return {
            'page_title': page_title,
            'display_region': display_region,
            'locale': locale,
            'page_url': View.gen_page_url(request),
            'contact_centre_number': View.get_contact_centre_number(display_region),
            'contact_us_link': View.get_campaign_site_link(request, display_region, 'contact-us'),
            'issue': issue
        }
