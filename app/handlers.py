import aiohttp_jinja2
from aiohttp.web import RouteTableDef, json_response
from structlog import get_logger

from app.security import forget
from app.utils import View

logger = get_logger('respondent-home')
static_routes = RouteTableDef()


@static_routes.view('/info', use_prefix=False)
class Info(View):
    async def get(self, _request):
        info = {
            'name': 'respondent-home-ui',
        }
        return json_response(info)


@static_routes.view(r'/' + View.valid_display_regions + '/signed-out/')
class SignedOut(View):
    @aiohttp_jinja2.template('signed-out.html')
    async def get(self, request):
        display_region = request.match_info['display_region']
        self.log_entry(request, display_region + '/signed-out')
        if display_region == 'cy':
            page_title = "PLACEHOLDER WELSH Progress saved"
            locale = 'cy'
        else:
            page_title = 'Progress saved'
            locale = 'en'
        await forget(request)
        return {
            'page_title': page_title,
            'display_region': display_region,
            'locale': locale,
            'page_url': View.gen_page_url(request)
        }


@static_routes.view(r'/' + View.valid_display_regions + '/cookies/')
class Cookies(View):
    @aiohttp_jinja2.template('cookies.html')
    async def get(self, request):
        display_region = request.match_info['display_region']
        locale = display_region
        self.log_entry(request, display_region + '/cookies/')
        return {
            'display_region': display_region,
            'locale': locale,
            'page_url': View.gen_page_url(request)
        }


@static_routes.view(r'/' + View.valid_display_regions + '/privacy-and-data-protection/')
class PrivacyAndDataProtection(View):
    @aiohttp_jinja2.template('privacy-and-data-protection.html')
    async def get(self, request):
        display_region = request.match_info['display_region']
        locale = display_region
        self.log_entry(request, display_region + '/privacy-and-data-protection/')
        return {
            'display_region': display_region,
            'locale': locale,
            'code_of_practice_link': View.get_campaign_site_link(request, display_region, 'code_of_practice_link'),
            'access_to_research_link': View.get_campaign_site_link(request, display_region, 'access_to_research_link'),
            'approved_researchers_link': View.get_campaign_site_link(request, display_region,
                                                                     'approved_researchers_link'),
            'ons_data_protection_link': View.get_campaign_site_link(request, display_region,
                                                                    'ons_data_protection_link'),
            'page_url': View.gen_page_url(request)
        }
