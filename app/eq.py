from aiohttp.web import Application, HTTPFound
from aiohttp.client_exceptions import (ClientResponseError)
from structlog import get_logger

from .exceptions import InvalidForEqTokenGeneration, TooManyRequestsEQLaunch
from .service_calls.rhsvc import RHSvc

logger = get_logger('respondent-home')


class EqLaunch(object):

    @staticmethod
    def get_account_service_url_and_logout(app: Application, display_region: str):
        domain_url_protocol = app['DOMAIN_URL_PROTOCOL']
        domain_url = app['DOMAIN_URL_EN']
        url_path_prefix = app['URL_PATH_PREFIX']
        url_display_region = '/' + display_region
        save_and_exit_url = '/signed-out/'
        start_url = '/start/'
        account_service_url = f'{domain_url_protocol}{domain_url}{url_path_prefix}{url_display_region}{start_url}'
        account_service_log_out_url = \
            f'{domain_url_protocol}{domain_url}{url_path_prefix}{url_display_region}{save_and_exit_url}'

        return account_service_url, account_service_log_out_url

    @staticmethod
    def url_path(uac_hash: str, display_region: str, app: Application):
        account_service_url, account_service_log_out_url = EqLaunch.get_account_service_url_and_logout(app, display_region)

        base = f'/eqLaunch/{uac_hash}'
        p1 = f'languageCode={display_region}'
        p2 = f'accountServiceUrl={account_service_url}'
        p3 = f'accountServiceLogoutUrl={account_service_log_out_url}'
        url = f'{base}?{p1}&{p2}&{p3}'
        return url

    @staticmethod
    async def call_eq(request, uac_hash: str, display_region: str, app: Application):
        try:
            url = EqLaunch.url_path(uac_hash, display_region, app)
            token = await RHSvc.get_eq_launch_token(request, url)
        except ClientResponseError as ex:
            if ex.status == 429:
                raise TooManyRequestsEQLaunch()
            else:
                raise ex

        logger.info('redirecting to eq',
                    client_ip=request['client_ip'], client_id=request['client_id'], trace=request['trace'])
        eq_url = app['EQ_URL']
        raise HTTPFound(f'{eq_url}/session?token={token}')
