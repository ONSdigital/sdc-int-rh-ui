from aiohttp.client_exceptions import (ClientResponseError)
from .exceptions import TooManyRequestsEQLaunch
from aiohttp.web import HTTPFound
from pytz import timezone

from app.service_calls.rhsvc import EQLaunch

from sdc.crypto.encrypter import encrypt
from .eq import EqPayloadConstructor
from structlog import get_logger

logger = get_logger('respondent-home')

uk_zone = timezone('Europe/London')


class View:
    valid_display_regions = r'{display_region:\ben|cy\b}'
    valid_display_regions_en_only = r'{display_region:\ben\b}'
    valid_user_journeys = r'{user_journey:\bstart|request\b}'
    page_title_error_prefix_en = 'Error: '
    page_title_error_prefix_cy = 'Gwall: '

    @staticmethod
    def log_entry(request, endpoint):
        method = request.method
        logger.info(f"received {method} on endpoint '{endpoint}'",
                    client_ip=request['client_ip'],
                    client_id=request['client_id'],
                    trace=request['trace'],
                    method=request.method,
                    path=request.path)

    @staticmethod
    def gen_page_url(request):
        full_url = str(request.rel_url)
        if full_url[:3] == '/en' or full_url[:3] == '/cy':
            generic_url = full_url[3:]
        else:
            generic_url = full_url
        return generic_url

    @staticmethod
    def get_contact_centre_number(display_region):
        if display_region == 'cy':
            contact_centre_number = '0800 169 2021'
        else:
            contact_centre_number = '0800 141 2021'
        return contact_centre_number

    @staticmethod
    def get_campaign_site_link(request, display_region, requested_link):
        base_en = request.app['DOMAIN_URL_PROTOCOL'] + request.app['DOMAIN_URL_EN']
        base_cy = request.app['DOMAIN_URL_PROTOCOL'] + request.app['DOMAIN_URL_CY']

        link = '/'

        if requested_link == 'surveys-home':
            if display_region == 'cy':
                link = base_cy
            else:
                link = base_en
        elif requested_link == 'contact-us':
            if display_region == 'cy':
                link = base_cy + '/cysylltu-a-ni/'
            else:
                link = base_en + '/contact-us/'
        elif requested_link == 'privacy':
            if display_region == 'cy':
                link = base_cy + '/preifatrwydd-a-diogelu-data/'
            else:
                link = base_en + '/privacy-and-data-protection/'

        return link


class LaunchEQ:
    @staticmethod
    async def call_questionnaire(request, case, attributes, app, adlocation):
        eq_payload = await EqPayloadConstructor(case, attributes, app).build()

        token = encrypt(eq_payload,
                        key_store=app['key_store'],
                        key_purpose='authentication')

        try:
            await EQLaunch.post_surveylaunched(request, case, adlocation)
        except ClientResponseError as ex:
            if ex.status == 429:
                raise TooManyRequestsEQLaunch()
            else:
                raise ex

        logger.info('redirecting to eq',
                    client_ip=request['client_ip'], client_id=request['client_id'], trace=request['trace'])
        eq_url = app['EQ_URL']
        raise HTTPFound(f'{eq_url}/session?token={token}')


class FlashMessage:
    @staticmethod
    def generate_flash_message(text, level, message_type, field):
        json_return = {'text': text, 'level': level, 'type': message_type, 'field': field}
        return json_return
