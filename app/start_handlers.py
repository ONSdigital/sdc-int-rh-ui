import re

import aiohttp_jinja2
from aiohttp import ClientResponseError
from aiohttp.web import HTTPFound, RouteTableDef
from aiohttp_session import get_session
from structlog import get_logger

from . import (BAD_CODE_MSG, INVALID_CODE_MSG, NO_SELECTION_CHECK_MSG,
               BAD_CODE_MSG_CY, INVALID_CODE_MSG_CY, NO_SELECTION_CHECK_MSG_CY,
               START_PAGE_TITLE_EN, START_PAGE_TITLE_CY)
from .eq import EqLaunch
from .exceptions import InvalidForEqTokenGeneration, InvalidAccessCode, InactiveUacError, AlreadyReceiptedUacError
from .flash import flash
from .security import remember, get_permitted_session, get_sha256_hash, invalidate
from .service_calls.rhsvc import RHSvc
from .session import get_session_value
from .utils import View

logger = get_logger('respondent-home')
start_routes = RouteTableDef()
user_journey = 'start'


class StartCommon(View):
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

    @staticmethod
    def validate_case(case_json):
        if not case_json.get('active', False):
            raise AlreadyReceiptedUacError()


@start_routes.view(r'/' + View.valid_display_regions + '/' + user_journey + '/')
class Start(StartCommon):
    @aiohttp_jinja2.template('start.html')
    async def get(self, request):
        display_region = request.match_info['display_region']
        self.log_entry(request, display_region + '/' + user_journey)
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

    # TODO should this have a template above it?
    # I don't understand why for the start page this had no template set for post, but Address Confirm did???
    # @aiohttp_jinja2.template('start.html')
    async def post(self, request):
        display_region = request.match_info['display_region']
        self.log_entry(request, display_region + '/' + user_journey)

        data = await request.post()

        if (not data.get('uac')) or (data.get('uac') == ''):
            return self._display_missing_uac_error(request, display_region)

        try:
            request['uac_hash'] = self.uac_hash(data.get('uac'))
        except TypeError:
            return self._display_malformed_uac_message(request, display_region)

        token = await EqLaunch.get_token(request, display_region)

        #     TODO: need to add back in checking the UAC is active, not receipted etc, etc
        # Should we do this server side, and give back a good answer? or keep as is
        EqLaunch.call_eq(request,token)


    @staticmethod
    def _display_malformed_uac_message(request, display_region):
        logger.warn('attempt to use a malformed access code',
                    client_ip=request['client_ip'], client_id=request['client_id'], trace=request['trace'])
        message = {
            'en': INVALID_CODE_MSG,
            'cy': INVALID_CODE_MSG_CY
        }[display_region]
        flash(request, message)
        return HTTPFound(request.app.router['Start:get'].url_for(display_region=display_region))

    @staticmethod
    def _display_missing_uac_error(request, display_region):
        logger.info('access code not supplied',
                    client_ip=request['client_ip'],
                    client_id=request['client_id'],
                    trace=request['trace'],
                    region_of_site=display_region)
        if display_region == 'cy':
            flash(request, BAD_CODE_MSG_CY)
        else:
            flash(request, BAD_CODE_MSG)

        return HTTPFound(request.app.router['Start:get'].url_for(display_region=display_region))

    # async def Oldpost(self, request):
    #     """
    #     Forward to Address confirmation
    #     :param request:
    #     :return: address confirmation view
    #     """
    #     display_region = request.match_info['display_region']
    #     self.log_entry(request, display_region + '/' + user_journey)
    #
    #     data = await request.post()
    #
    #     if (not data.get('uac')) or (data.get('uac') == ''):
    #         logger.info('access code not supplied',
    #                     client_ip=request['client_ip'],
    #                     client_id=request['client_id'],
    #                     trace=request['trace'],
    #                     region_of_site=display_region)
    #         if display_region == 'cy':
    #             flash(request, BAD_CODE_MSG_CY)
    #         else:
    #             flash(request, BAD_CODE_MSG)
    #         return HTTPFound(request.app.router['Start:get'].url_for(display_region=display_region))
    #
    #     try:
    #         request['uac_hash'] = self.uac_hash(data.get('uac'))
    #     except TypeError:
    #         logger.warn('attempt to use a malformed access code',
    #                     client_ip=request['client_ip'], client_id=request['client_id'], trace=request['trace'])
    #         message = {
    #             'en': INVALID_CODE_MSG,
    #             'cy': INVALID_CODE_MSG_CY
    #         }[display_region]
    #         flash(request, message)
    #         return HTTPFound(request.app.router['Start:get'].url_for(display_region=display_region))
    #
    #     try:
    #         uac_context = await RHSvc.get_uac_details(request)
    #     except ClientResponseError as ex:
    #         if ex.status == 404:
    #             logger.warn('attempt to use an invalid access code',
    #                         client_ip=request['client_ip'], client_id=request['client_id'], trace=request['trace'])
    #             if display_region == 'cy':
    #                 flash(request, INVALID_CODE_MSG_CY)
    #             else:
    #                 flash(request, INVALID_CODE_MSG)
    #             raise InvalidAccessCode
    #         else:
    #             logger.error('error processing access code',
    #                          client_ip=request['client_ip'], client_id=request['client_id'], trace=request['trace'])
    #             raise ex
    #
    #     if uac_context['receiptReceived']:
    #         raise InactiveCaseError
    #     elif not uac_context['active']:
    #         collection_id = uac_context['collectionExercise']['collectionExerciseId']
    #         raise ExerciseClosedError(collection_id)
    #     else:
    #         await remember(uac_context['collectionCase']['caseId'], request)
    #         self.validate_case(uac_context)
    #
    #     try:
    #         auth_attributes = uac_context['collectionCase']['sample']
    #     except KeyError:
    #         raise InvalidForEqTokenGeneration('Could not retrieve address details')
    #
    #     logger.debug('address confirmation displayed',
    #                  client_ip=request['client_ip'], client_id=request['client_id'], trace=request['trace'])
    #     session = await get_session(request)
    #     session['auth_attributes'] = auth_attributes
    #     session['uac_context'] = uac_context
    #
    #     return HTTPFound(request.app.router['StartConfirmAddress:get'].url_for(display_region=display_region))


@start_routes.view(r'/' + View.valid_display_regions + '/' + user_journey + '/confirm-address/')
class StartConfirmAddress(StartCommon):
    @aiohttp_jinja2.template('start-confirm-address.html')
    async def get(self, request):
        """
        Address Confirmation get.
        """
        display_region = request.match_info['display_region']
        self.log_entry(request, display_region + '/' + user_journey + '/confirm-address')

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

        auth_attributes = get_session_value(request, session, 'auth_attributes', user_journey)

        return {'locale': locale,
                'page_title': page_title,
                'page_url': View.gen_page_url(request),
                'display_region': display_region,
                'addressLine1': get_session_value(request, auth_attributes, 'addressLine1', user_journey),
                'addressLine2': get_session_value(request, auth_attributes, 'addressLine2', user_journey),
                'addressLine3': get_session_value(request, auth_attributes, 'addressLine3', user_journey),
                'townName': get_session_value(request, auth_attributes, 'townName', user_journey),
                'postcode': get_session_value(request, auth_attributes, 'postcode', user_journey)
                }

    @aiohttp_jinja2.template('start-confirm-address.html')
    async def post(self, request):
        """
        Address Confirmation flow. If correct address will build EQ payload and send to EQ.
        """
        session = await get_permitted_session(request)
        display_region = request.match_info['display_region']
        self.log_entry(request, display_region + '/' + user_journey + '/confirm-address')

        data = await request.post()
        if display_region == 'cy':
            locale = 'cy'
        else:
            locale = 'en'

        auth_attributes = get_session_value(request, session, 'auth_attributes', user_journey)
        uac_context = get_session_value(request, session, 'uac_context', user_journey)

        try:
            address_confirmation = data['address-check-answer']
        except KeyError:
            logger.info('address confirmation error',
                        client_ip=request['client_ip'],
                        client_id=request['client_id'],
                        trace=request['trace'],
                        region_of_site=display_region,
                        postcode=get_session_value(request, auth_attributes, 'postcode', user_journey))
            if display_region == 'cy':
                flash(request, NO_SELECTION_CHECK_MSG_CY)
            else:
                flash(request, NO_SELECTION_CHECK_MSG)

            return HTTPFound(
                request.app.router['StartConfirmAddress:get'].url_for(display_region=display_region))

        if address_confirmation == 'Yes':
            auth_attributes['language'] = locale
            auth_attributes['display_region'] = display_region
            await EqLaunch(uac_context, auth_attributes, request.app).call_eq(request)

        elif address_confirmation == 'No':
            return HTTPFound(request.app.router['StartIncorrectAddress:get'].url_for(display_region=display_region))

        else:
            # catch all just in case, should never get here
            logger.info('address confirmation error',
                        client_ip=request['client_ip'],
                        client_id=request['client_id'],
                        trace=request['trace'],
                        user_selection=address_confirmation,
                        region_of_site=display_region,
                        postcode=get_session_value(request, auth_attributes, 'postcode', user_journey))
            if display_region == 'cy':
                flash(request, NO_SELECTION_CHECK_MSG_CY)
            else:
                flash(request, NO_SELECTION_CHECK_MSG)
            return HTTPFound(
                request.app.router['StartConfirmAddress:get'].url_for(display_region=display_region))


@start_routes.view(r'/' + View.valid_display_regions + '/' + user_journey + '/exit/')
class StartExit(StartCommon):
    async def get(self, request):
        display_region = request.match_info['display_region']
        self.log_entry(request, display_region + '/' + user_journey + '/exit')
        await invalidate(request)
        return HTTPFound(
            request.app.router['Start:get'].url_for(display_region=display_region)
        )


@start_routes.view(r'/' + View.valid_display_regions + '/' + user_journey + '/incorrect-address/')
class StartIncorrectAddress(View):
    @aiohttp_jinja2.template('start-incorrect-address.html')
    async def get(self, request):
        display_region = request.match_info['display_region']

        if display_region == 'cy':
            page_title = "You do not need to take part in this study"
            locale = 'cy'
        else:
            page_title = 'You do not need to take part in this study'
            locale = 'en'

        self.log_entry(request, display_region + '/' + user_journey + '/incorrect-address')

        return {
            'page_title': page_title,
            'display_region': display_region,
            'locale': locale,
            'page_url': View.gen_page_url(request),
        }
