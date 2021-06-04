import aiohttp_jinja2

from aiohttp.web import HTTPFound, RouteTableDef
from structlog import get_logger

from .utils import View

logger = get_logger('respondent-home')
common_routes = RouteTableDef()

# common_handlers contains routes and supporting code for any route in more than top level journey path
# eg start or request


@common_routes.view(r'/' + View.valid_display_regions + '/' + View.valid_user_journeys
                    + '/call-contact-centre/')
class CommonCallContactCentre(View):
    """
    Common route to render a 'Call the Contact Centre' page from any journey
    """
    @aiohttp_jinja2.template('common-contact-centre.html')
    async def get(self, request):
        display_region = request.match_info['display_region']
        user_journey = request.match_info['user_journey']

        if display_region == 'cy':
            page_title = "Ffoniwch Canolfan Gyswllt i Gwsmeriaid y Cyfrifiad"
            locale = 'cy'
        else:
            page_title = 'Call Census Customer Contact Centre'
            locale = 'en'

        self.log_entry(request, display_region + '/' + user_journey + '/call-contact-centre')

        return {
            'page_title': page_title,
            'display_region': display_region,
            'locale': locale,
            'user_journey': user_journey,
            'page_url': View.gen_page_url(request),
            'call_centre_number': View.get_call_centre_number(display_region)
        }
