import aiohttp
from aiohttp.client_exceptions import (ClientConnectionError,
                                       ClientConnectorError,
                                       ClientResponseError)

from tenacity import (retry,
                      stop_after_attempt,
                      retry_if_exception_message,
                      retry_if_exception_type,
                      wait_exponential,
                      RetryError)
from structlog import get_logger

logger = get_logger('respondent-home')

pooled_attempts_limit = 2
basic_attempt_limit = 3
wait_multiplier = 0.01


def after_failed_attempt(request_type, retry_state):
    logger.warn(request_type + ' request attempt failed', attempts=retry_state.attempt_number)


def after_failed_basic(retry_state):
    after_failed_attempt('basic', retry_state)


def after_failed_pooled(retry_state):
    after_failed_attempt('pooled', retry_state)


class RetryRequest:
    """
    Make requests to a URL, but retry under certain conditions to tolerate server graceful shutdown.
    """

    def __init__(self, request, method, url, auth, request_headers, request_json, return_type):
        self.request = request
        self.method = method
        self.url = url
        self.auth = auth
        self.headers = request_headers
        self.json = request_json
        self.return_type = return_type

    async def __handle_response(self, response):
        try:
            body = None
            if self.return_type == 'text':
                body = await response.text()
            elif self.return_type == 'json':
                body = await response.json()

            response.raise_for_status()
        except ClientResponseError as ex:
            ex.message = body
            raise ex
        else:
            logger.debug('successfully connected to service',
                         client_ip=self.request['client_ip'],
                         client_id=self.request['client_id'],
                         trace=self.request['trace'],
                         url=self.url)

        return body

    @retry(reraise=True, stop=stop_after_attempt(basic_attempt_limit),
           wait=wait_exponential(multiplier=wait_multiplier, exp_base=25),
           after=after_failed_basic,
           retry=(retry_if_exception_message(match='503.*') | retry_if_exception_type((ClientConnectionError,
                                                                                       ClientConnectorError))))
    async def _request_basic(self):
        # basic request without keep-alive to avoid terminating service.
        logger.info('request using basic connection',
                    client_ip=self.request['client_ip'],
                    client_id=self.request['client_id'],
                    trace=self.request['trace'])

        try:
            async with aiohttp.request(
                    self.method, self.url, auth=self.auth, json=self.json, headers=self.headers) as resp:
                return self.__handle_response(resp)
        except ClientConnectionError as ex:
            raise ex

    @retry(stop=stop_after_attempt(pooled_attempts_limit),
           wait=wait_exponential(multiplier=wait_multiplier),
           after=after_failed_pooled,
           retry=(retry_if_exception_message(match='503.*') | retry_if_exception_type((ClientConnectionError,
                                                                                       ClientConnectorError))))
    async def _request_using_pool(self):
        async with self.request.app.http_session_pool.request(
                self.method, self.url, auth=self.auth, json=self.json, headers=self.headers, ssl=False) as resp:
            return await self.__handle_response(resp)

    async def make_request(self):
        """
        Make a request with retries.
        First the fast pooled connection will be tried, but if certain failures are detected, then it will be retried.
        If the retry limit is reached then a basic connection will be tried (and retried if necessary)
        Finally the error will be propagated.
        """
        logger.debug('making request with handler',
                     client_ip=self.request['client_ip'],
                     client_id=self.request['client_id'],
                     trace=self.request['trace'],
                     method=self.method,
                     url=self.url)
        try:
            try:
                return await self._request_using_pool()
            except RetryError as retry_ex:
                attempts = retry_ex.last_attempt.attempt_number
                logger.warn('Could not make request using normal pooled connection',
                            client_ip=self.request['client_ip'],
                            client_id=self.request['client_id'],
                            trace=self.request['trace'],
                            attempts=attempts)
                return await self._request_basic()
        except ClientResponseError as ex:
            if ex.status not in [400, 404, 429]:
                logger.error('error in response',
                             client_ip=self.request['client_ip'],
                             client_id=self.request['client_id'],
                             trace=self.request['trace'],
                             url=self.url,
                             status_code=ex.status)
            elif ex.status == 429:
                self.log_too_many_requests(ex)
            elif ex.status == 400:
                logger.warn('bad request',
                            client_ip=self.request['client_ip'],
                            client_id=self.request['client_id'],
                            trace=self.request['trace'],
                            url=self.url,
                            status_code=ex.status)
            raise ex
        except (ClientConnectionError, ClientConnectorError) as ex:
            logger.error('client failed to connect',
                         client_ip=self.request['client_ip'],
                         client_id=self.request['client_id'],
                         trace=self.request['trace'],
                         url=self.url)
            raise ex

    def log_too_many_requests(self, ex: ClientResponseError):
        ai_svc_url = self.request.app['ADDRESS_INDEX_SVC_URL']
        ai_svc_ext_url = self.request.app['ADDRESS_INDEX_SVC_EXTERNAL_URL']
        tracking = {"client_ip": self.request['client_ip'], "client_id": self.request['client_id'],
                    "trace": self.request['trace']}
        if (ai_svc_url in self.url) or (ai_svc_ext_url in self.url):
            logger.error('error in AIMS response',
                         **tracking,
                         url=self.url,
                         status_code=ex.status)
        else:
            logger.warn('too many requests',
                        **tracking,
                        url=self.url,
                        status_code=ex.status)
