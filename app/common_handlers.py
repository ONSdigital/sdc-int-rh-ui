import aiohttp_jinja2

from aiohttp.web import HTTPFound, RouteTableDef
from structlog import get_logger
from aiohttp_session import get_session
from aiohttp.client_exceptions import (ClientResponseError)

from . import (ADDRESS_SELECT_CHECK_MSG,
               ADDRESS_SELECT_CHECK_MSG_CY,
               NO_SELECTION_CHECK_MSG,
               NO_SELECTION_CHECK_MSG_CY)

from .flash import flash
from .security import get_permitted_session, forget
from .utils import View, ProcessPostcode, InvalidDataError, InvalidDataErrorWelsh, FlashMessage, AddressIndex, RHService
from .session import get_existing_session, get_session_value

logger = get_logger('respondent-home')
common_routes = RouteTableDef()

# common_handlers contains routes and supporting code for any route in more than top level journey path
# eg start or request


@common_routes.view(r'/' + View.valid_display_regions + '/' + View.valid_user_journeys
                    + '/' + View.valid_sub_user_journeys + '/register-address/')
class CommonRegisterAddress(View):
    """
    Common route to render the 'Register address' page from any journey
    """
    @aiohttp_jinja2.template('common-register-address.html')
    async def get(self, request):
        display_region = request.match_info['display_region']
        user_journey = request.match_info['user_journey']
        sub_user_journey = request.match_info['sub_user_journey']

        if display_region == 'cy':
            page_title = 'Cofrestru cyfeiriad'
            locale = 'cy'
        else:
            page_title = 'Register address'
            locale = 'en'

        self.log_entry(request, display_region + '/' + user_journey + '/' + sub_user_journey + '/register-address')

        return {
            'page_title': page_title,
            'display_region': display_region,
            'locale': locale,
            'page_url': View.gen_page_url(request),
            'contact_us_link': View.get_campaign_site_link(request, display_region, 'contact-us'),
            'call_centre_number': View.get_call_centre_number(display_region)
        }


@common_routes.view(r'/' + View.valid_display_regions + '/' + View.valid_user_journeys
                    + '/call-contact-centre/{error}/')
class CommonCallContactCentre(View):
    """
    Common route to render a 'Call the Contact Centre' page from any journey
    """
    @aiohttp_jinja2.template('common-contact-centre.html')
    async def get(self, request):
        display_region = request.match_info['display_region']
        user_journey = request.match_info['user_journey']
        error = request.match_info['error']

        if display_region == 'cy':
            page_title = "Ffoniwch Canolfan Gyswllt i Gwsmeriaid y Cyfrifiad"
            locale = 'cy'
        else:
            page_title = 'Call Census Customer Contact Centre'
            locale = 'en'

        self.log_entry(request, display_region + '/' + user_journey + '/call-contact-centre/' + error)

        return {
            'page_title': page_title,
            'display_region': display_region,
            'locale': locale,
            'user_journey': user_journey,
            'error': error,
            'page_url': View.gen_page_url(request),
            'call_centre_number': View.get_call_centre_number(display_region)
        }


@common_routes.view(r'/' + View.valid_display_regions + '/' + View.valid_user_journeys
                    + '/' + View.valid_sub_user_journeys + '/enter-address/')
class CommonEnterAddress(View):
    """
    Common route to enable address entry via postcode from start and request journeys
    """
    @aiohttp_jinja2.template('common-enter-address.html')
    async def get(self, request):
        display_region = request.match_info['display_region']
        user_journey = request.match_info['user_journey']
        sub_user_journey = request.match_info['sub_user_journey']

        self.log_entry(request, display_region + '/' + user_journey + '/' + sub_user_journey + '/enter-address')

        if user_journey == 'start':
            session = await get_permitted_session(request)
        else:
            session = await get_session(request)

        individual = False

        if user_journey == 'start':
            session['attributes']['individual'] = False
            session.changed()
            individual = False
        elif user_journey == 'request':
            await forget(request)  # Removes identity in case user has existing auth session
            try:
                individual = session['attributes']['individual']
            except KeyError:
                individual = False
                attributes = {'individual': False}
                session['attributes'] = attributes

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
            'sub_user_journey': sub_user_journey,
            'locale': locale,
            'page_url': View.gen_page_url(request),
            'contact_us_link': View.get_campaign_site_link(request, display_region, 'contact-us'),
            'individual': individual
        }

    async def post(self, request):
        display_region = request.match_info['display_region']
        user_journey = request.match_info['user_journey']
        sub_user_journey = request.match_info['sub_user_journey']

        self.log_entry(request, display_region + '/' + user_journey + '/' + sub_user_journey + '/enter-address')

        if user_journey == 'start':
            session = await get_permitted_session(request)
        else:
            session = await get_existing_session(request, user_journey, sub_user_journey)

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
                request.app.router['CommonEnterAddress:get'].url_for(
                    display_region=display_region,
                    user_journey=user_journey,
                    sub_user_journey=sub_user_journey
                ))

        session['attributes']['postcode'] = postcode
        session.changed()

        raise HTTPFound(
            request.app.router['CommonSelectAddress:get'].url_for(
                display_region=display_region,
                user_journey=user_journey,
                sub_user_journey=sub_user_journey
            ))


@common_routes.view(r'/' + View.valid_display_regions + '/' + View.valid_user_journeys
                    + '/' + View.valid_sub_user_journeys + '/select-address/')
class CommonSelectAddress(View):
    """
    Common route to enable address selection from start and request journeys
    """
    @aiohttp_jinja2.template('common-select-address.html')
    async def get(self, request):
        display_region = request.match_info['display_region']
        user_journey = request.match_info['user_journey']
        sub_user_journey = request.match_info['sub_user_journey']

        self.log_entry(request, display_region + '/' + user_journey + '/' + sub_user_journey + '/select-address')

        if user_journey == 'start':
            session = await get_permitted_session(request)
        else:
            session = await get_existing_session(request, user_journey, sub_user_journey)

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

        attributes = get_session_value(session, 'attributes', user_journey, sub_user_journey)
        postcode = attributes['postcode']

        address_content = await AddressIndex.get_postcode_return(request, postcode, display_region)
        address_content['page_title'] = page_title
        address_content['display_region'] = display_region
        address_content['user_journey'] = user_journey
        address_content['sub_user_journey'] = sub_user_journey
        address_content['locale'] = locale
        address_content['page_url'] = View.gen_page_url(request)
        address_content['contact_us_link'] = View.get_campaign_site_link(request, display_region, 'contact-us')
        address_content['call_centre_number'] = View.get_call_centre_number(display_region)

        return address_content

    async def post(self, request):
        display_region = request.match_info['display_region']
        user_journey = request.match_info['user_journey']
        sub_user_journey = request.match_info['sub_user_journey']

        self.log_entry(request, display_region + '/' + user_journey + '/' + sub_user_journey + '/select-address')

        if user_journey == 'start':
            session = await get_permitted_session(request)
        else:
            session = await get_existing_session(request, user_journey, sub_user_journey)

        attributes = get_session_value(session, 'attributes', user_journey, sub_user_journey)

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
                request.app.router['CommonSelectAddress:get'].url_for(
                    display_region=display_region,
                    user_journey=user_journey,
                    sub_user_journey=sub_user_journey
                ))

        if selected_uprn == 'xxxx':
            raise HTTPFound(
                request.app.router['CommonRegisterAddress:get'].url_for(
                    display_region=display_region,
                    user_journey=user_journey,
                    sub_user_journey=sub_user_journey))
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
            request.app.router['CommonConfirmAddress:get'].url_for(
                display_region=display_region,
                user_journey=user_journey,
                sub_user_journey=sub_user_journey
            ))


@common_routes.view(r'/' + View.valid_display_regions + '/' + View.valid_user_journeys
                    + '/' + View.valid_sub_user_journeys + '/confirm-address/')
class CommonConfirmAddress(View):
    """
    Common route to enable address confirmation from start and request journeys
    """
    @aiohttp_jinja2.template('common-confirm-address.html')
    async def get(self, request):
        display_region = request.match_info['display_region']
        user_journey = request.match_info['user_journey']
        sub_user_journey = request.match_info['sub_user_journey']

        self.log_entry(request, display_region + '/' + user_journey + '/' + sub_user_journey + '/confirm-address')

        if user_journey == 'start':
            session = await get_permitted_session(request)
        else:
            session = await get_existing_session(request, user_journey, sub_user_journey)

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

        attributes = get_session_value(session, 'attributes', user_journey, sub_user_journey)
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
            'sub_user_journey': sub_user_journey,
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
        user_journey = request.match_info['user_journey']
        sub_user_journey = request.match_info['sub_user_journey']

        self.log_entry(request, display_region + '/' + user_journey + '/' + sub_user_journey + '/confirm-address')

        if user_journey == 'start':
            session = await get_permitted_session(request)
        else:
            session = await get_existing_session(request, user_journey, sub_user_journey)

        attributes = get_session_value(session, 'attributes', user_journey, sub_user_journey)

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
                request.app.router['CommonConfirmAddress:get'].url_for(
                    display_region=display_region,
                    user_journey=user_journey,
                    sub_user_journey=sub_user_journey
                ))

        if address_confirmation == 'yes':

            if attributes.get('case_id'):
                raise HTTPFound(
                    request.app.router['RequestCodeSelectHowToReceive:get'].url_for(
                        request_type=sub_user_journey, display_region=display_region))
            else:
                logger.info('no case', **tracking)
                raise HTTPFound(
                    request.app.router['CommonCallContactCentre:get'].url_for(
                        display_region=display_region, user_journey=user_journey, error='no_case'))

        elif address_confirmation == 'no':

            raise HTTPFound(
                request.app.router['CommonEnterAddress:get'].url_for(display_region=display_region,
                                                                     user_journey=user_journey,
                                                                     sub_user_journey=sub_user_journey))

        else:
            # catch all just in case, should never get here
            logger.info('address confirmation error', **tracking, user_selection=address_confirmation)
            flash(request, NO_SELECTION_CHECK_MSG)
            raise HTTPFound(
                request.app.router['CommonConfirmAddress:get'].url_for(
                    display_region=display_region,
                    user_journey=user_journey,
                    sub_user_journey=sub_user_journey
                ))
