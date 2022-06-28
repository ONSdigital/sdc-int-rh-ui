from aiohttp.web import Application, HTTPFound
from aiohttp.client_exceptions import (ClientResponseError)
from structlog import get_logger

from .exceptions import InvalidForEqTokenGeneration, TooManyRequestsEQLaunch
from .service_calls.rhsvc import RHSvc


logger = get_logger('respondent-home')


class EqLaunch(object):
    """
    Encapsulate the setup and call to EQ.
    """
    def __init__(self, uac_hash: str, display_region: str, app: Application):
        """
        Creates the attributes needed to call the RH Service to get the EQ token for launch
        """
        self._app = app
        self._uac_hash = uac_hash

        domain_url_protocol = app['DOMAIN_URL_PROTOCOL']
        domain_url = app['DOMAIN_URL_EN']
        url_path_prefix = app['URL_PATH_PREFIX']
        url_display_region = '/' + display_region
        save_and_exit_url = '/signed-out/'
        start_url = '/start/'
        self._account_service_url = \
            f'{domain_url_protocol}{domain_url}{url_path_prefix}{url_display_region}{start_url}'
        self._account_service_log_out_url = \
            f'{domain_url_protocol}{domain_url}{url_path_prefix}{url_display_region}{save_and_exit_url}'

        self._language_code = display_region

    def url_path(self):
        """ build the URL path for calling RHSvc to get the EQ token """
        base = f'/eqLaunch/{self._uac_hash}'
        p1 = f'languageCode={self._language_code}'
        p2 = f'accountServiceUrl={self._account_service_url}'
        p3 = f'accountServiceLogoutUrl={self._account_service_log_out_url}'
        url = f'{base}?{p1}&{p2}&{p3}'
        return url

    # TODO: make this a static? just pass in the data required and call functions to build UrlPath
    # why bother with building with an init 1st
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
