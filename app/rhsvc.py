from app.request import RetryRequest
from structlog import get_logger

logger = get_logger('respondent-home')


class RHSvc:
    @staticmethod
    async def get_eq_launch_token(request, url_path):
        rhsvc_url = request.app['RHSVC_URL']
        url = f'{rhsvc_url}{url_path}'

        retry_request = RetryRequest(request, 'GET', url, request.app['RHSVC_AUTH'], None, None, "text")
        return await retry_request.make_request()
