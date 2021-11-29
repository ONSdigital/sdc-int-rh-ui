import re
from app.request import RetryRequest
from structlog import get_logger

logger = get_logger('respondent-home')


class MakeRequest:
    @staticmethod
    async def make_request(request,
                           method,
                           url,
                           auth=None,
                           headers=None,
                           request_json=None,
                           return_json=False):
        """
        :param request: The AIOHTTP user request, used for logging and app access
        :param method: The HTTP verb
        :param url: The target URL
        :param auth: Authorization
        :param headers: Any needed headers as a python dictionary
        :param request_json: JSON payload to pass as request data
        :param return_json: If True, the response JSON will be returned
        """
        retry_request = RetryRequest(request, method, url, auth, headers, request_json, return_json)
        return await retry_request.make_request()


class SingleClientIP:
    @staticmethod
    def single_client_ip(request):
        if request['client_ip']:
            client_ip = request['client_ip']
            single_ip_validation_pattern = re.compile(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$')
            if client_ip.count(',') > 1:
                single_ip_value = client_ip.split(', ', -1)[-3]
                if single_ip_validation_pattern.fullmatch(single_ip_value):
                    single_ip = single_ip_value
                else:
                    logger.warn('clientIP failed validation. Provided IP - ' + client_ip,
                                client_id=request['client_id'],
                                trace=request['trace'])
                    single_ip = ''
            else:
                logger.warn('clientIP failed validation. Provided IP - ' + client_ip,
                            client_id=request['client_id'],
                            trace=request['trace'])
                single_ip = ''
        elif request.headers.get('Origin', None) and 'localhost' in request.headers.get('Origin', None):
            single_ip = '127.0.0.1'
        else:
            single_ip = ''
        return single_ip
