import aiohttp_jinja2
from aiohttp.web import RouteTableDef
from structlog import get_logger

from .utils import View

logger = get_logger('respondent-home')
register_routes = RouteTableDef()


@register_routes.view(r'/' + View.valid_display_regions_en_only + '/register/')
class Register(View):
    @aiohttp_jinja2.template('register.html')
    async def get(self, request):
        display_region = 'en'
        page_title = 'Take part in a survey'
        if request.get('flash'):
            page_title = View.page_title_error_prefix_en + page_title
        locale = 'en'
        self.log_entry(request, display_region + '/register')

        return {
            'display_region': display_region,
            'page_title': page_title,
            'locale': locale,
            'page_url': View.gen_page_url(request),
        }
