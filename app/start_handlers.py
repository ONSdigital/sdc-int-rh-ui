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

    @aiohttp_jinja2.template('start.html')
    async def post(self, request):
        display_region = request.match_info['display_region']
        self.log_entry(request, display_region + '/' + user_journey)

        data = await request.post()

        if (not data.get('uac')) or (data.get('uac') == ''):
            return self._display_missing_uac_error(request, display_region)

        try:
            request['uac_hash'] = self._uac_hash(data.get('uac'))
        except TypeError:
            return self._display_malformed_uac_message(request, display_region)

        token = await EqLaunch.get_token(request, display_region)
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
    def _uac_hash(uac, expected_length=16):
        if uac:
            combined = uac.upper().replace(' ', '')
        else:
            combined = ''

        uac_validation_pattern = re.compile(r'^[A-Z0-9]{16}$')

        if (len(combined) < expected_length) or not (uac_validation_pattern.fullmatch(combined)):  # yapf: disable
            raise TypeError

        return get_sha256_hash(combined)

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


@start_routes.view(r'/' + View.valid_display_regions + '/' + user_journey + '/exit/')
class StartExit(StartCommon):
    async def get(self, request):
        display_region = request.match_info['display_region']
        self.log_entry(request, display_region + '/' + user_journey + '/exit')
        await invalidate(request)
        return HTTPFound(
            request.app.router['Start:get'].url_for(display_region=display_region)
        )
