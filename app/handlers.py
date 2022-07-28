import aiohttp_jinja2

from aiohttp.web import RouteTableDef, json_response, FileResponse
from structlog import get_logger

from . import VERSION
from .security import forget
from .utils import View

logger = get_logger('respondent-home')
static_routes = RouteTableDef()


@static_routes.view('/info', use_prefix=False)
class Info(View):
    async def get(self, request):
        info = {
            'name': 'respondent-home-ui',
            'version': VERSION,
        }
        if 'check' in request.query:
            info['ready'] = await request.app.check_services()
        return json_response(info)


@static_routes.view(r'/' + View.valid_display_regions + '/signed-out/')
class SignedOut(View):
    @aiohttp_jinja2.template('signed-out.html')
    async def get(self, request):
        display_region = request.match_info['display_region']
        self.log_entry(request, display_region + '/signed-out')
        if display_region == 'cy':
            page_title = "Cynnydd wedi'i gadw"
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


@static_routes.view('/data/schools/')
class SchoolsData(View):
    async def get(self, request):
        return FileResponse('app/data/schools.json')


@static_routes.view('/cookies/')
class Cookies(View):
    @aiohttp_jinja2.template('cookies.html')
    async def get(self, request):
        return {
            'page_url': View.gen_page_url(request)
        }


@static_routes.view('/privacy-and-data-protection/')
class PrivacyAndDataProtection(View):
    @aiohttp_jinja2.template('privacy-and-data-protection.html')
    async def get(self, request):
        return {
            'page_url': View.gen_page_url(request)
        }
