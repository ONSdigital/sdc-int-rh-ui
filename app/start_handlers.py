import aiohttp_jinja2
import re
import uuid

from aiohttp.client_exceptions import (ClientResponseError)
from aiohttp.web import HTTPFound, RouteTableDef
from aiohttp_session import get_session
from structlog import get_logger

from . import (BAD_CODE_MSG, INVALID_CODE_MSG, NO_SELECTION_CHECK_MSG,
               BAD_CODE_MSG_CY, INVALID_CODE_MSG_CY, NO_SELECTION_CHECK_MSG_CY,
               START_PAGE_TITLE_EN, START_PAGE_TITLE_CY)

from .flash import flash

from .exceptions import InvalidEqPayLoad, InvalidAccessCode
from .security import remember, get_permitted_session, get_sha256_hash, invalidate
from .session import get_session_value

from .utils import View, RHService

logger = get_logger('respondent-home')
start_routes = RouteTableDef()


class StartCommon(View):
    def setup_uac_hash(self, request, uac, lang):
        try:
            request['uac_hash'] = self.uac_hash(uac)
        except TypeError:
            logger.warn('attempt to use a malformed access code',
                        client_ip=request['client_ip'], client_id=request['client_id'], trace=request['trace'])
            message = {
                'en': INVALID_CODE_MSG,
                'cy': INVALID_CODE_MSG_CY
            }[lang]
            flash(request, message)
            raise HTTPFound(request.app.router['Start:get'].url_for(display_region=lang))

    @staticmethod
    def uac_hash(uac, expected_length=16):
        if uac:
            combined = uac.upper().replace(' ', '')
        else:
            combined = ''

        uac_validation_pattern = re.compile(r'^[A-Z0-9]{16}$')

        if (len(combined) < expected_length) or not (uac_validation_pattern.fullmatch(combined)):  # yapf: disable
            raise TypeError

        return get_sha256_hash(combined)


@start_routes.view(r'/' + View.valid_display_regions + '/start/')
class Start(StartCommon):
    @aiohttp_jinja2.template('start.html')
    async def get(self, request):
        """
        RH home page to enter a UAC.
        Checks if URL carries query string assisted digital location and stores to session
        :param request:
        :return:
        """
        display_region = request.match_info['display_region']
        self.log_entry(request, display_region + '/start')
        if display_region == 'cy':
            locale = 'cy'
            page_title = START_PAGE_TITLE_CY
            if request.get('flash'):
                page_title = View.page_title_error_prefix_cy + page_title
        else:
            locale = 'en'
            page_title = START_PAGE_TITLE_EN
            if request.get('flash'):
                page_title = View.page_title_error_prefix_en + page_title

        return {
            'display_region': display_region,
            'page_title': page_title,
            'locale': locale,
            'page_url': View.gen_page_url(request)
        }

    async def post(self, request):
        """
        Forward to Address confirmation
        :param request:
        :return: address confirmation view
        """
        display_region = request.match_info['display_region']
        self.log_entry(request, display_region + '/start')

        data = await request.post()

        if (not data.get('uac')) or (data.get('uac') == ''):
            logger.info('access code not supplied',
                        client_ip=request['client_ip'],
                        client_id=request['client_id'],
                        trace=request['trace'],
                        region_of_site=display_region)
            if display_region == 'cy':
                flash(request, BAD_CODE_MSG_CY)
            else:
                flash(request, BAD_CODE_MSG)
            raise HTTPFound(request.app.router['Start:get'].url_for(display_region=display_region))

        self.setup_uac_hash(request, data.get('uac'), lang=display_region)

        try:
            uac_json = await RHService.get_uac_details(request)
        except ClientResponseError as ex:
            if ex.status == 404:
                logger.warn('attempt to use an invalid access code',
                            client_ip=request['client_ip'], client_id=request['client_id'], trace=request['trace'])
                if display_region == 'cy':
                    flash(request, INVALID_CODE_MSG_CY)
                else:
                    flash(request, INVALID_CODE_MSG)
                raise InvalidAccessCode
            else:
                logger.error('error processing access code',
                             client_ip=request['client_ip'], client_id=request['client_id'], trace=request['trace'])
                raise ex

        await remember(uac_json['caseId'], request)

        self.validate_case(uac_json)

        try:
            attributes = uac_json['address']
        except KeyError:
            raise InvalidEqPayLoad('Could not retrieve address details')

        logger.debug('address confirmation displayed',
                     client_ip=request['client_ip'], client_id=request['client_id'], trace=request['trace'])
        session = await get_session(request)
        session['attributes'] = attributes
        session['case'] = uac_json

        raise HTTPFound(request.app.router['StartConfirmAddress:get'].url_for(display_region=display_region))


@start_routes.view(r'/' + View.valid_display_regions + '/start/confirm-address/')
class StartConfirmAddress(StartCommon):
    @aiohttp_jinja2.template('start-confirm-address.html')
    async def get(self, request):
        """
        Address Confirmation get.
        """
        display_region = request.match_info['display_region']
        self.log_entry(request, display_region + '/start/confirm-address')

        session = await get_permitted_session(request)

        if display_region == 'cy':
            page_title = "Cadarnhau cyfeiriad"
            if request.get('flash'):
                page_title = View.page_title_error_prefix_cy + page_title
            locale = 'cy'
        else:
            page_title = 'Confirm address'
            if request.get('flash'):
                page_title = View.page_title_error_prefix_en + page_title
            locale = 'en'

        attributes = get_session_value(session, 'attributes', 'start')

        return {'locale': locale,
                'page_title': page_title,
                'page_url': View.gen_page_url(request),
                'display_region': display_region,
                'addressLine1': attributes['addressLine1'],
                'addressLine2': attributes['addressLine2'],
                'addressLine3': attributes['addressLine3'],
                'townName': attributes['townName'],
                'postcode': attributes['postcode']
                }

    @aiohttp_jinja2.template('start-confirm-address.html')
    async def post(self, request):
        """
        Address Confirmation flow. If correct address will build EQ payload and send to EQ.
        """
        session = await get_permitted_session(request)
        display_region = request.match_info['display_region']
        self.log_entry(request, display_region + '/start/confirm-address')

        data = await request.post()
        if display_region == 'cy':
            locale = 'cy'
        else:
            locale = 'en'

        attributes = get_session_value(session, 'attributes', 'start')
        case = get_session_value(session, 'case', 'start')

        try:
            address_confirmation = data['address-check-answer']
        except KeyError:
            logger.info('address confirmation error',
                        client_ip=request['client_ip'],
                        client_id=request['client_id'],
                        trace=request['trace'],
                        region_of_site=display_region,
                        postcode=attributes['postcode'])
            if display_region == 'cy':
                flash(request, NO_SELECTION_CHECK_MSG_CY)
            else:
                flash(request, NO_SELECTION_CHECK_MSG)

            raise HTTPFound(
                request.app.router['StartConfirmAddress:get'].url_for(display_region=display_region))

        if address_confirmation == 'Yes':
            attributes['language'] = locale
            attributes['display_region'] = display_region
            await self.call_questionnaire(request, case, attributes,
                                          request.app,
                                          session.get('adlocation'))

        elif address_confirmation == 'No':
            raise HTTPFound(request.app.router['CommonEnterAddress:get'].url_for(
                display_region=display_region,
                user_journey='start',
                sub_user_journey='change-address'
            ))

        else:
            # catch all just in case, should never get here
            logger.info('address confirmation error',
                        client_ip=request['client_ip'],
                        client_id=request['client_id'],
                        trace=request['trace'],
                        user_selection=address_confirmation,
                        region_of_site=display_region,
                        postcode=attributes['postcode'])
            if display_region == 'cy':
                flash(request, NO_SELECTION_CHECK_MSG_CY)
            else:
                flash(request, NO_SELECTION_CHECK_MSG)
            raise HTTPFound(
                request.app.router['StartConfirmAddress:get'].url_for(display_region=display_region))


@start_routes.view(r'/' + View.valid_display_regions + '/start/exit/')
class StartExit(StartCommon):
    async def get(self, request):
        display_region = request.match_info['display_region']
        self.log_entry(request, display_region + '/start/exit')
        await invalidate(request)
        raise HTTPFound(
            request.app.router['Start:get'].url_for(display_region=display_region)
        )
