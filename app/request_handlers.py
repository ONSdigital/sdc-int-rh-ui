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

from .exceptions import TooManyRequests
from .security import invalidate

from .utils import View, ProcessPostcode, ProcessMobileNumber, InvalidDataError, InvalidDataErrorWelsh, \
    FlashMessage, AddressIndex, RHService, ProcessName
from .session import get_existing_session, get_session_value

logger = get_logger('respondent-home')
request_routes = RouteTableDef()

user_journey = 'request'
valid_request_types = r'{request_type:\baccess-code\b}'


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
            page_title = 'Nodi cyfeiriad'
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
            'contact_us_link': View.get_campaign_site_link(request, display_region, 'contact-us')
        }

    async def post(self, request):
        display_region = request.match_info['display_region']
        request_type = request.match_info['request_type']

        self.log_entry(request, display_region + '/' + user_journey + '/' + request_type + '/enter-address')

        session = await get_existing_session(request, user_journey, request_type)

        data = await request.post()

        try:
            postcode = ProcessPostcode.validate_postcode(data['form-enter-address-postcode'], display_region)
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
            raise HTTPFound(
                request.app.router['RequestEnterAddress:get'].url_for(
                    display_region=display_region,
                    user_journey=user_journey,
                    request_type=request_type
                ))

        attributes = {'postcode': postcode}
        session['attributes'] = attributes
        session.changed()

        raise HTTPFound(
            request.app.router['RequestSelectAddress:get'].url_for(
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

        attributes = get_session_value(session, 'attributes', user_journey, request_type)
        postcode = attributes['postcode']

        address_content = await AddressIndex.get_postcode_return(request, postcode, display_region)
        address_content['page_title'] = page_title
        address_content['display_region'] = display_region
        address_content['user_journey'] = user_journey
        address_content['request_type'] = request_type
        address_content['locale'] = locale
        address_content['page_url'] = View.gen_page_url(request)
        address_content['contact_us_link'] = View.get_campaign_site_link(request, display_region, 'contact-us')
        address_content['call_centre_number'] = View.get_call_centre_number(display_region)

        return address_content

    async def post(self, request):
        display_region = request.match_info['display_region']
        request_type = request.match_info['request_type']

        self.log_entry(request, display_region + '/' + user_journey + '/' + request_type + '/select-address')

        session = await get_existing_session(request, user_journey, request_type)

        attributes = get_session_value(session, 'attributes', user_journey, request_type)

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
            raise HTTPFound(
                request.app.router['RequestSelectAddress:get'].url_for(
                    display_region=display_region,
                    user_journey=user_journey,
                    request_type=request_type
                ))

        if selected_uprn == 'xxxx':
            raise HTTPFound(
                request.app.router['RequestRegisterAddress:get'].url_for(
                    display_region=display_region,
                    user_journey=user_journey,
                    request_type=request_type))
        else:
            attributes['uprn'] = selected_uprn
            session.changed()
            logger.info('session updated',
                        client_ip=request['client_ip'],
                        client_id=request['client_id'],
                        trace=request['trace'],
                        uprn_selected=selected_uprn,
                        region_of_site=display_region)

        raise HTTPFound(
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

        attributes = get_session_value(session, 'attributes', user_journey, request_type)
        uprn = attributes['uprn']

        try:
            rhsvc_uprn_return = await RHService.get_case_by_uprn(request, uprn)
            logger.info('case matching uprn found in RHSvc',
                        client_ip=request['client_ip'],
                        client_id=request['client_id'],
                        trace=request['trace'])
            attributes['addressLine1'] = rhsvc_uprn_return['addressLine1']
            attributes['addressLine2'] = rhsvc_uprn_return['addressLine2']
            attributes['addressLine3'] = rhsvc_uprn_return['addressLine3']
            attributes['townName'] = rhsvc_uprn_return['townName']
            attributes['postcode'] = rhsvc_uprn_return['postcode']
            attributes['uprn'] = rhsvc_uprn_return['uprn']
            attributes['case_id'] = rhsvc_uprn_return['caseId']
            attributes['region'] = rhsvc_uprn_return['region']

            session.changed()

        except ClientResponseError as ex:
            if ex.status == 404:
                logger.info('no case matching uprn in RHSvc - call contact centre page',
                            client_ip=request['client_ip'],
                            client_id=request['client_id'],
                            trace=request['trace'])
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
            'addressLine1': attributes['addressLine1'],
            'addressLine2': attributes['addressLine2'],
            'addressLine3': attributes['addressLine3'],
            'townName': attributes['townName'],
            'postcode': attributes['postcode']
        }

    async def post(self, request):
        tracking = {"client_ip": request['client_ip'], "client_id": request['client_id'], "trace": request['trace']}

        display_region = request.match_info['display_region']
        request_type = request.match_info['request_type']

        self.log_entry(request, display_region + '/' + user_journey + '/' + request_type + '/confirm-address')

        session = await get_existing_session(request, user_journey, request_type)

        attributes = get_session_value(session, 'attributes', user_journey, request_type)

        data = await request.post()

        try:
            address_confirmation = data['form-confirm-address']
        except KeyError:
            logger.info('address confirmation error', **tracking, region_of_site=display_region)
            if display_region == 'cy':
                flash(request, NO_SELECTION_CHECK_MSG_CY)
            else:
                flash(request, NO_SELECTION_CHECK_MSG)
            raise HTTPFound(
                request.app.router['RequestConfirmAddress:get'].url_for(
                    display_region=display_region,
                    user_journey=user_journey,
                    request_type=request_type
                ))

        if address_confirmation == 'yes':

            if attributes.get('case_id'):
                raise HTTPFound(
                    request.app.router['RequestCodeSelectHowToReceive:get'].url_for(
                        request_type=request_type, display_region=display_region))
            else:
                logger.info('no case', **tracking)
                raise HTTPFound(
                    request.app.router['CommonCallContactCentre:get'].url_for(
                        display_region=display_region, user_journey=user_journey))

        elif address_confirmation == 'no':

            raise HTTPFound(
                request.app.router['RequestEnterAddress:get'].url_for(display_region=display_region,
                                                                      user_journey=user_journey,
                                                                      request_type=request_type))

        else:
            # catch all just in case, should never get here
            logger.info('address confirmation error', **tracking, user_selection=address_confirmation)
            flash(request, NO_SELECTION_CHECK_MSG)
            raise HTTPFound(
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

        session = await get_existing_session(request, 'request', request_type)
        attributes = get_session_value(session, 'attributes', 'request', request_type)

        if display_region == 'cy':
            page_title = 'Select how to receive access code'
            if request.get('flash'):
                page_title = View.page_title_error_prefix_cy + page_title
            locale = 'cy'
        else:
            page_title = 'Select how to receive access code'
            if request.get('flash'):
                page_title = View.page_title_error_prefix_en + page_title
            locale = 'en'

        attributes['page_title'] = page_title
        attributes['display_region'] = display_region
        attributes['locale'] = locale
        attributes['request_type'] = request_type
        attributes['page_url'] = View.gen_page_url(request)
        attributes['contact_us_link'] = View.get_campaign_site_link(request, display_region, 'contact-us')

        return attributes

    async def post(self, request):

        request_type = request.match_info['request_type']
        display_region = request.match_info['display_region']

        await get_existing_session(request, 'request', request_type)

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
            raise HTTPFound(
                request.app.router['RequestCodeSelectHowToReceive:get'].url_for(
                    display_region=display_region,
                    request_type=request_type
                ))

        if request_method == 'sms':
            raise HTTPFound(
                request.app.router['RequestCodeEnterMobile:get'].url_for(request_type=request_type,
                                                                         display_region=display_region))

        elif request_method == 'post':
            raise HTTPFound(
                request.app.router['RequestCommonEnterName:get'].url_for(request_type=request_type,
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
            raise HTTPFound(
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

        session = await get_existing_session(request, 'request', request_type)
        attributes = get_session_value(session, 'attributes',  'request', request_type)

        attributes['page_title'] = page_title
        attributes['display_region'] = display_region
        attributes['locale'] = locale
        attributes['request_type'] = request_type
        attributes['page_url'] = View.gen_page_url(request)

        return attributes

    async def post(self, request):
        request_type = request.match_info['request_type']
        display_region = request.match_info['display_region']

        if display_region == 'cy':
            locale = 'cy'
        else:
            locale = 'en'

        self.log_entry(request, display_region + '/request/' + request_type + '/enter-mobile')

        session = await get_existing_session(request, 'request', request_type)
        attributes = get_session_value(session, 'attributes', 'request', request_type)

        data = await request.post()

        try:
            mobile_number = ProcessMobileNumber.validate_uk_mobile_phone_number(data['request-mobile-number'],
                                                                                locale)

            logger.info('valid mobile number',
                        client_ip=request['client_ip'], client_id=request['client_id'], trace=request['trace'])

            attributes['mobile_number'] = mobile_number
            attributes['submitted_mobile_number'] = data['request-mobile-number']
            session.changed()

            raise HTTPFound(
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
            raise HTTPFound(
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

        self.log_entry(request, display_region + '/request/' + request_type + '/confirm-send-by-text')

        session = await get_existing_session(request, 'request', request_type)
        attributes = get_session_value(session, 'attributes', 'request', request_type)

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

        attributes['page_title'] = page_title
        attributes['display_region'] = display_region
        attributes['locale'] = locale
        attributes['request_type'] = request_type
        attributes['page_url'] = View.gen_page_url(request)

        return attributes

    async def post(self, request):

        request_type = request.match_info['request_type']
        display_region = request.match_info['display_region']

        self.log_entry(request, display_region + '/request/' + request_type + '/confirm-send-by-text')

        session = await get_existing_session(request, 'request', request_type)
        attributes = get_session_value(session, 'attributes', 'request', request_type)

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
            raise HTTPFound(
                request.app.router['RequestCodeConfirmSendByText:get'].url_for(
                    display_region=display_region,
                    request_type=request_type
                ))

        if mobile_confirmation == 'yes':

            fulfilment_individual = 'false'

            if display_region == 'cy':
                fulfilment_language = 'W'
            else:
                fulfilment_language = 'E'

            logger.info(f"fulfilment query: region={attributes['region']}, "
                        f"individual={fulfilment_individual}",
                        client_ip=request['client_ip'],
                        client_id=request['client_id'],
                        trace=request['trace'],
                        postcode=attributes['postcode'])

            fulfilment_code_array = []

            try:
                available_fulfilments = await RHService.get_fulfilment(
                    request, 'HH', attributes['region'], 'SMS', 'UAC', fulfilment_individual)
                if len(available_fulfilments) > 1:
                    for fulfilment in available_fulfilments:
                        if fulfilment['language'] == fulfilment_language:
                            fulfilment_code_array.append(fulfilment['fulfilmentCode'])
                else:
                    fulfilment_code_array.append(available_fulfilments[0]['fulfilmentCode'])

                try:
                    await RHService.request_fulfilment_sms(request,
                                                           attributes['case_id'],
                                                           attributes['mobile_number'],
                                                           fulfilment_code_array)
                except (KeyError, ClientResponseError) as ex:
                    if ex.status == 429:
                        raise TooManyRequests(request_type)
                    else:
                        raise ex

                raise HTTPFound(
                    request.app.router['RequestCodeSentByText:get'].url_for(request_type=request_type,
                                                                            display_region=display_region))
            except ClientResponseError as ex:
                raise ex

        elif mobile_confirmation == 'no':
            raise HTTPFound(
                request.app.router['RequestCodeEnterMobile:get'].url_for(request_type=request_type,
                                                                         display_region=display_region))

        else:
            # catch all just in case, should never get here
            logger.info('mobile confirmation error',
                        client_ip=request['client_ip'],
                        client_id=request['client_id'],
                        trace=request['trace'],
                        user_selection=mobile_confirmation)
            flash(request, NO_SELECTION_CHECK_MSG)
            raise HTTPFound(
                request.app.router['RequestCodeConfirmSendByText:get'].url_for(
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

        session = await get_existing_session(request, 'request', request_type)
        attributes = get_session_value(session, 'attributes', 'request', request_type)

        attributes['page_title'] = page_title
        attributes['display_region'] = display_region
        attributes['locale'] = locale
        attributes['request_type'] = request_type
        attributes['page_url'] = View.gen_page_url(request)

        return attributes

    async def post(self, request):
        request_type = request.match_info['request_type']
        display_region = request.match_info['display_region']

        self.log_entry(request, display_region + '/request/' + request_type + '/enter-name')

        session = await get_existing_session(request, 'request', request_type)
        attributes = get_session_value(session, 'attributes', 'request', request_type)

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
                request.app.router['RequestCommonEnterName:get'].url_for(
                    display_region=display_region,
                    request_type=request_type
                ))

        name_first_name = data['name_first_name'].strip()
        name_last_name = data['name_last_name'].strip()

        attributes['first_name'] = name_first_name
        attributes['last_name'] = name_last_name
        session.changed()

        raise HTTPFound(
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

        session = await get_existing_session(request, 'request', request_type)
        attributes = get_session_value(session, 'attributes', 'request', request_type)

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
            'first_name': attributes['first_name'],
            'last_name': attributes['last_name'],
            'addressLine1': attributes['addressLine1'],
            'addressLine2': attributes['addressLine2'],
            'addressLine3': attributes['addressLine3'],
            'townName': attributes['townName'],
            'postcode': attributes['postcode']
        }

    async def post(self, request):
        request_type = request.match_info['request_type']
        display_region = request.match_info['display_region']

        self.log_entry(request, display_region + '/request/' + request_type + '/confirm-send-by-post')

        session = await get_existing_session(request, 'request', request_type)
        attributes = get_session_value(session, 'attributes', 'request', request_type)

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

            raise HTTPFound(
                request.app.router['RequestCommonConfirmSendByPost:get'].url_for(display_region=display_region,
                                                                                 request_type=request_type))

        if name_address_confirmation == 'yes':

            fulfilment_individual = 'false'

            if display_region == 'cy':
                fulfilment_language = 'W'
            else:
                fulfilment_language = 'E'

            fulfilment_code_array = []

            try:
                available_fulfilments = await RHService.get_fulfilment(
                    request,
                    'HH',
                    attributes['region'],
                    'POST',
                    'UAC',
                    fulfilment_individual)

                if len(available_fulfilments) > 1:
                    for fulfilment in available_fulfilments:
                        if fulfilment['language'] == fulfilment_language:
                            fulfilment_code_array.append(fulfilment['fulfilmentCode'])
                else:
                    fulfilment_code_array.append(available_fulfilments[0]['fulfilmentCode'])

                logger.info(
                    f"fulfilment query: region={attributes['region']}, individual={fulfilment_individual}",
                    client_ip=request['client_ip'],
                    client_id=request['client_id'],
                    trace=request['trace'],
                    postcode=attributes['postcode'])

                try:
                    await RHService.request_fulfilment_post(request,
                                                            attributes['case_id'],
                                                            attributes['first_name'],
                                                            attributes['last_name'],
                                                            fulfilment_code_array,
                                                            None)
                except (KeyError, ClientResponseError) as ex:
                    if ex.status == 429:
                        raise TooManyRequests(request_type)
                    else:
                        raise ex

                raise HTTPFound(
                    request.app.router['RequestCodeSentByPost:get'].url_for(display_region=display_region,
                                                                            request_type=request_type))

            except ClientResponseError as ex:
                raise ex

        elif name_address_confirmation == 'no':
            raise HTTPFound(
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
                flash(request, FlashMessage.generate_flash_message('Dewiswch ateb',
                                                                   'ERROR',
                                                                   'NAME_CONFIRMATION_ERROR',
                                                                   'request-name-confirmation'))
            else:
                flash(request, FlashMessage.generate_flash_message('Select an answer',
                                                                   'ERROR',
                                                                   'NAME_CONFIRMATION_ERROR',
                                                                   'request-name-confirmation'))

            raise HTTPFound(
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

        session = await get_existing_session(request, 'request', request_type)
        attributes = get_session_value(session, 'attributes', 'request', request_type)

        if display_region == 'cy':
            page_title = "Access code has been sent by text"
            locale = 'cy'
        else:
            page_title = 'Access code has been sent by text'
            locale = 'en'

        attributes['page_title'] = page_title
        attributes['display_region'] = display_region
        attributes['locale'] = locale
        attributes['request_type'] = request_type
        attributes['page_url'] = View.gen_page_url(request)

        await invalidate(request)

        return attributes


@request_routes.view(r'/' + View.valid_display_regions + '/' + user_journey + '/' + valid_request_types +
                     '/code-sent-by-post/')
class RequestCodeSentByPost(View):
    @aiohttp_jinja2.template('request-code-sent-by-post.html')
    async def get(self, request):

        request_type = request.match_info['request_type']
        display_region = request.match_info['display_region']

        self.log_entry(request, display_region + '/request/' + request_type + '/code-sent-by-post')

        session = await get_existing_session(request, 'request', request_type)
        attributes = get_session_value(session, 'attributes', 'request', request_type)

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
                'census_home_link': View.get_campaign_site_link(request, display_region, 'census-home'),
                'first_name': attributes['first_name'],
                'last_name': attributes['last_name'],
                'addressLine1': attributes['addressLine1'],
                'addressLine2': attributes['addressLine2'],
                'addressLine3': attributes['addressLine3'],
                'townName': attributes['townName'],
                'postcode': attributes['postcode']
            }


@request_routes.view(r'/' + View.valid_display_regions + '/' + user_journey + '/' + valid_request_types +
                     '/register-address/')
class RequestRegisterAddress(View):
    @aiohttp_jinja2.template('request-register-address.html')
    async def get(self, request):
        display_region = request.match_info['display_region']
        request_type = request.match_info['request_type']

        if display_region == 'cy':
            page_title = 'Cofrestru cyfeiriad'
            locale = 'cy'
        else:
            page_title = 'Register address'
            locale = 'en'

        self.log_entry(request, display_region + '/' + user_journey + '/' + request_type + '/register-address')

        return {
            'page_title': page_title,
            'display_region': display_region,
            'locale': locale,
            'page_url': View.gen_page_url(request),
            'contact_us_link': View.get_campaign_site_link(request, display_region, 'contact-us'),
            'call_centre_number': View.get_call_centre_number(display_region)
        }
