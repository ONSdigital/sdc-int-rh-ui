from app.request import RetryRequest


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
