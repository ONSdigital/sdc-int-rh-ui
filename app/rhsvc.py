from structlog import get_logger

from app.request import RetryRequest

logger = get_logger('respondent-home')


class RHSvc:
    @staticmethod
    async def get_eq_launch_token(request, url_path: str):
        rhsvc_url = request.app['RHSVC_URL']
        url = f'{rhsvc_url}{url_path}'

        retry_request = RetryRequest(originating_request=request, method='GET', url=url, return_type="text")
        return await retry_request.make_request()
