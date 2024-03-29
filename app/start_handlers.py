import re

import aiohttp_jinja2
from aiohttp.web import HTTPFound, RouteTableDef
from structlog import get_logger

from app.constants import (BAD_CODE_MSG, BAD_CODE_MSG_CY, INVALID_CODE_MSG, INVALID_CODE_MSG_CY, START_PAGE_TITLE_CY,
                           START_PAGE_TITLE_EN, UAC_LENGTH, BAD_CODE_LENGTH_MSG, BAD_CODE_LENGTH_MSG_CY)
from app.eq import EqLaunch
from app.flash import flash
from app.security import get_sha256_hash, invalidate
from app.utils import View

logger = get_logger('respondent-home')
start_routes = RouteTableDef()
user_journey = 'start'


@start_routes.view(r'/' + View.valid_display_regions + '/' + user_journey + '/')
class Start(View):
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

        uac = data.get('uac')
        if not uac:
            return self._display_missing_uac_error(request, display_region)

        combined_uac = uac.upper().replace(' ', '')
        if len(combined_uac) < UAC_LENGTH:
            return self._display_malformed_uac_message(request, display_region, BAD_CODE_LENGTH_MSG,
                                                       BAD_CODE_LENGTH_MSG_CY)

        try:
            request['uac_hash'] = self._uac_hash(combined_uac)
        except TypeError:
            return self._display_malformed_uac_message(request, display_region, INVALID_CODE_MSG, INVALID_CODE_MSG_CY)

        token = await EqLaunch.get_token(request, display_region, request.app)
        EqLaunch.call_eq(request.app['EQ_URL'], token)

    @staticmethod
    def _display_malformed_uac_message(request, display_region, malformed_uac_msg_en, malformed_uac_msg_cy):
        logger.warn('attempt to use a malformed access code',
                    client_ip=request['client_ip'], client_id=request['client_id'], trace=request['trace'])
        message = {
            'en': malformed_uac_msg_en,
            'cy': malformed_uac_msg_cy
        }[display_region]
        flash(request, message)
        return HTTPFound(request.app.router['Start:get'].url_for(display_region=display_region))

    @staticmethod
    def _uac_hash(uac):
        uac_validation_pattern = re.compile(fr'^[A-Z0-9]{{{UAC_LENGTH}}}$')   # Outer 2 curly braces escape the f-string

        if not uac_validation_pattern.fullmatch(uac):  # yapf: disable
            raise TypeError

        return get_sha256_hash(uac)

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
class StartExit(View):
    async def get(self, request):
        display_region = request.match_info['display_region']
        self.log_entry(request, display_region + '/' + user_journey + '/exit')
        await invalidate(request)
        return HTTPFound(
            request.app.router['Start:get'].url_for(display_region=display_region)
        )
