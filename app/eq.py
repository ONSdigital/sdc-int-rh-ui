from collections import namedtuple
from aiohttp.web import Application, HTTPFound
from aiohttp.client_exceptions import (ClientResponseError)
from structlog import get_logger

from .exceptions import InvalidForEqTokenGeneration, TooManyRequestsEQLaunch
from .service_calls.rhsvc import RHSvc


# FIXME is this Request thing needed ?
Request = namedtuple('Request', ['method', 'path', 'auth', 'func'])

logger = get_logger('respondent-home')


class EqLaunch(object):
    """
    Encapsulate the setup and call to EQ.
    """
    def __init__(self, uac_context: dict, attributes: dict, app: Application):
        """
        Creates the attributes needed to call the RH Service to get the EQ token for launch
        """

        self._app = app

        if not attributes:
            raise InvalidForEqTokenGeneration('Attributes is empty')

        self._sample_attributes = attributes
        self._uac_hash = uac_context['uacHash']

        domain_url_protocol = app['DOMAIN_URL_PROTOCOL']
        domain_url = app['DOMAIN_URL_EN']
        url_path_prefix = app['URL_PATH_PREFIX']
        url_display_region = '/' + self._sample_attributes['display_region']
        save_and_exit_url = '/signed-out/'
        start_url = '/start/'
        self._account_service_url = \
            f'{domain_url_protocol}{domain_url}{url_path_prefix}{url_display_region}{start_url}'
        self._account_service_log_out_url = \
            f'{domain_url_protocol}{domain_url}{url_path_prefix}{url_display_region}{save_and_exit_url}'

        try:
            self._region = uac_context['collectionCase']['sample']['region'][0]
        except KeyError:
            raise InvalidForEqTokenGeneration('Could not retrieve region from UAC context JSON')

        if self._region == 'E':
            self._language_code = 'en'
        else:
            self._language_code = self._sample_attributes['language']

    def url_path(self):
        """ build the URL path for calling RHSvc to get the EQ token """
        base = f'/uacs/{self._uac_hash}/launch'
        p1 = f'languageCode={self._language_code}'
        p2 = f'accountServiceUrl={self._account_service_url}'
        p3 = f'accountServiceLogoutUrl={self._account_service_log_out_url}'
        url = f'{base}?{p1}&{p2}&{p3}'
        return url

    async def call_eq(self, request):
        try:
            token = await RHSvc.get_eq_launch_token(request, self.url_path())
        except ClientResponseError as ex:
            if ex.status == 429:
                raise TooManyRequestsEQLaunch()
            else:
                raise ex

        logger.info('redirecting to eq',
                    client_ip=request['client_ip'], client_id=request['client_id'], trace=request['trace'])
        eq_url = self._app['EQ_URL']
        raise HTTPFound(f'{eq_url}/session?token={token}')
