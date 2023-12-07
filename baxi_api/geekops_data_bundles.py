from .geekops_base import geekopsBase
from .geekops_exceptions import ServerError, TransactionError, AirtimeProviderError, AirtimeRequestError
import requests
from urllib.parse import urlencode
import urllib.parse as urlparse
import json


from datetime import datetime
from babel.dates import format_datetime

now = datetime.utcnow()
format = 'EEE, dd LLL yyyy hh:mm:ss'
date = format_datetime(now, format, locale='en') + ' GMT'


class DataBundles(geekopsBase):
    """
    class to handle data bundles requests such as getting list of service providers
    and also making purchasing for data bundles. 
    """

    def __init__(self, apiKey):
        self.headers = {
            'content-type': 'application/json',
            'x-api-key': 'apikey',
            'accept': 'application/json',
            'baxi-date': str(date)
        }
        super(DataBundles, self).__init__(apiKey)

    def _handleDataBundlesRequests(self, endpoint, method, data=None):
        # check response method
        if method == 'GET':
            if data == None:
                response = requests.get(
                    endpoint, headers=self.headers, timeout=5)
            else:
                response = requests.get(
                    endpoint, headers=self.headers, data=json.dumps(data), timeout=5)

        if method == 'POST':
            if data == None:
                response = requests.post(
                    endpoint, headers=self.headers, timeout=15)

            else:
                response = requests.post(
                    url=endpoint, headers=self.headers, data=json.dumps(data), timeout=15)
                print(response.text)

        try:
            responseJson = response.json()
        except:
            raise ServerError({"error": True, "errMsg": response.text})

        return {"data": responseJson}
    # Functons to handle Data Bundles Requests

    def service_providers(self):
        endpoint = self._baseUrl + \
            self._endPoint['data_bundles']['list_providers']

        method = 'GET'

        return self._handleDataBundlesRequests(endpoint, method, data=None)

    def data_bundles(self, details):
        endpoint = self._baseUrl + \
            self._endPoint['data_bundles']['list_data_bundles']
        data = details

        # Parse url to include details
        # url_parts = list(urlparse.urlparse(endpoint))
        # query = dict(urlparse.parse_qsl(url_parts[4]))
        # query.update(details)
        # url_parts[4] = urlencode(query)
        # endpoint = urlparse.urlunparse(url_parts)

        method = 'POST'

        return self._handleDataBundlesRequests(endpoint, method, data=data)

    def request_data_bundles(self, details):
        endpoint = self._baseUrl + \
            self._endPoint['data_bundles']['data_bundles_request']
        data = details

        # Parse url to include details
        # url_parts = list(urlparse.urlparse(endpt))
        # query = dict(urlparse.parse_qsl(url_parts[4]))
        # query.update(details)
        # url_parts[4] = urlencode(query)
        # endpoint = urlparse.urlunparse(url_parts)

        method = 'POST'
        return self._handleDataBundlesRequests(endpoint, method, details)
