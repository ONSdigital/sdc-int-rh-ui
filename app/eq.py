from aiohttp.client_exceptions import (ClientResponseError)
from aiohttp.web import Application, HTTPFound
from structlog import get_logger

from app.constants import INVALID_CODE_MSG, INVALID_CODE_MSG_CY
from app.exceptions import AlreadyReceiptedUacError, InactiveUacError, InvalidAccessCode, TooManyRequestsEQLaunch
from app.flash import flash
from app.rhsvc import RHSvc

logger = get_logger('respondent-home')


class EqLaunch(object):
    @staticmethod
    def call_eq(eq_url, token: str):
        # 'raise HTTPFound is the valid AIO way of redirecting
        raise HTTPFound(f'{eq_url}/session?token={token}')

    @staticmethod
    async def get_token(request, display_region: str, app):
        try:
            url = EqLaunch._url_path(request['uac_hash'], display_region, app)
            token = await RHSvc.get_eq_launch_token(request, url)
        except ClientResponseError as ex:
            if ex.status == 404:
                logger.warn('attempt to use an invalid access code',
                            client_ip=request['client_ip'], client_id=request['client_id'], trace=request['trace'])
                if display_region == 'cy':
                    flash(request, INVALID_CODE_MSG_CY)
                else:
                    flash(request, INVALID_CODE_MSG)

                raise InvalidAccessCode

            if ex.status == 400:
                if ex.message == 'UAC_RECEIPTED':
                    logger.error('attempt to use receipted UAC',
                                 client_ip=request['client_ip'], client_id=request['client_id'], trace=request['trace'])
                    raise AlreadyReceiptedUacError
                if ex.message == 'UAC_INACTIVE':
                    logger.error('attempt to use inactive UAC',
                                 client_ip=request['client_ip'], client_id=request['client_id'], trace=request['trace'])
                    raise InactiveUacError

                raise ex

            if ex.status == 429:
                raise TooManyRequestsEQLaunch
            else:
                logger.error('error processing access code',
                             status='ex.status', client_ip=request['client_ip'],
                             client_id=request['client_id'], trace=request['trace'])
                raise ex

        return token

    @staticmethod
    def _url_path(uac_hash: str, display_region: str, app: Application):
        account_service_url = EqLaunch._get_account_service_url(app,
                                                                display_region)
        base = f'/eqLaunch/{uac_hash}'
        p1 = f'languageCode={display_region}'
        p2 = f'accountServiceUrl={account_service_url}'
        url = f'{base}?{p2}&{p1}'
        return url

    @staticmethod
    def _get_account_service_url(app: Application, display_region: str):
        domain_url_protocol = app['DOMAIN_URL_PROTOCOL']
        domain_url = app['DOMAIN_URL']
        url_path_prefix = app['URL_PATH_PREFIX']
        account_service_url = f'{domain_url_protocol}{domain_url}{url_path_prefix}'

        return account_service_url
