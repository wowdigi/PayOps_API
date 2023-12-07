from .geekops_base import geekopsBase
from .geekops_exceptions import ServerError, TransactionError, AirtimeProviderError, AirtimeRequestError
import requests
from urllib.parse import urlencode
import urllib.parse as urlparse
import json


class Airtime(geekopsBase):
    """
    class to handle airtime requests such as getting list of service providers
    and also making airtime request
    . 
    """

    def __init__(self, apiKey):
        self.headers = {
            'Content-Type': 'application/json',
            'x-api-key': 'apiKeyFromENV',
            'Accept': 'application/json',
        }
        super(Airtime, self).__init__(apiKey)

    def _handleAirtimeRequests(self, endpoint, method, data=None):
        # check response method
        if method == 'GET':
            if data == None:
                response = requests.get(
                    endpoint, headers=self.headers, timeout=10)
            else:
                response = requests.get(
                    endpoint, headers=self.headers, data=json.dumps(data), timeout=10)

        if method == 'POST':
            if data == None:
                response = requests.post(
                    endpoint, headers=self.headers, timeout=10)

            else:
                response = requests.post(
                    endpoint, headers=self.headers, data=json.dumps(data), timeout=10)

        try:
            responseJson = response.json()
            print(responseJson)
        except:
            raise ServerError({"error": True, "errMsg": response.text})

        return {"data": responseJson}

    # Functons to handle Airtime Requests

    def service_providers(self):
        endpoint = self._baseUrl + self._endPoint['airtime']['list_providers']

        method = 'GET'

        return self._handleAirtimeRequests(endpoint, method, data=None)

    def request_airtime(self, details):
        endpt = "https://api.baxibap.com/services/airtime/request"

        # data = details

        # # Parse url to include service_type
        # url_parts = list(urlparse.urlparse(endpt))
        # query = dict(urlparse.parse_qsl(url_parts[4]))
        # query.update(details)
        # url_parts[4] = urlencode(query)
        # endpoint = urlparse.urlunparse(url_parts)

        method = 'POST'
        return self._handleAirtimeRequests(endpt, method, details)
