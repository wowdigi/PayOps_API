from .geekops_base import geekopsBase
from .geekops_exceptions import ServerError, TransactionError, AirtimeProviderError, AirtimeRequestError
import requests
from urllib.parse import urlencode
import urllib.parse as urlparse
import json


class Electricity(geekopsBase):
    """
    class to handle data bundle requests such as getting list of service providers
    and also making purchasing for data bundle. 
    """

    def __init__(self, apiKey):
        self.headers = {
           'content-type': 'application/json',
            'x-api-key': 'api-key',
            'accept': 'application/json',
        }
        super(Electricity, self).__init__(apiKey)

    def _handleElectricityRequests(self, endpoint, method, data=None):
        # check response method
        if method == 'GET':
            if data == None:
                response = requests.get(
                    endpoint, headers=self.headers, timeout=3)
            else:
                response = requests.get(
                    endpoint, headers=self.headers, data=json.dumps(data), timeout=3)

        if method == 'POST':
            if data == None:
                response = requests.post(
                    endpoint, headers=self.headers, timeout=3)

            else:
                response = requests.post(
                    endpoint, headers=self.headers, data=json.dumps(data), timeout=3)
                print(response.text)

        try:
            responseJson = response.json()
        except:
            raise ServerError({"error": True, "errMsg": response.text})

        return {"data": responseJson}

    # Functons to handle Data Bundle Requests

    def electricity_billers(self):
        endpoint = self._baseUrl + \
            self._endPoint['electricity']['electricity_billers']

        method = 'GET'

        return self._handleElectricityRequests(endpoint, method, data=None)

    def verify_user(self, details):
        endpoint = self._baseUrl + self._endPoint['electricity']['verify_user']
        data = details

        # Parse url to include details
        url_parts = list(urlparse.urlparse(endpoint))
        query = dict(urlparse.parse_qsl(url_parts[4]))
        query.update(details)
        url_parts[4] = urlencode(query)
        endpoint = urlparse.urlunparse(url_parts)

        method = 'POST'

        return self._handleElectricityRequests(endpoint, method, data=data)

    def request_electricity(self, details):
        endpt = 'https://api.staging.baxibap.com/services/electricity/request'
        data = details

        # Parse url to include details
        # url_parts = list(urlparse.urlparse(endpt))
        # query = dict(urlparse.parse_qsl(url_parts[4]))
        # query.update(details)
        # url_parts[4] = urlencode(query)
        # endpoint = urlparse.urlunparse(url_parts)

        method = 'POST'
        return self._handleElectricityRequests(endpt, method, data=data)
