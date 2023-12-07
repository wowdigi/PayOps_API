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


class CableTv(geekopsBase):
    """
    class to handle data bundle requests such as getting list of service providers
    and also making purchasing for data bundle.
    """

    def __init__(self, apiKey):
        self.headers = {
            'content-type': 'application/json',
            'x-api-key': 'apikey',
            'accept': 'application/json',
            'Baxi-date': str(date),
        }
        super(CableTv, self).__init__(apiKey)

    def _handleCableTvRequests(self, endpoint, method, data=None):
        # check response method
        url = 'https://api.staging.baxibap.com/services/multichoice/request'
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
                    endpoint, headers=self.headers, data=json.dumps(data), timeout=10)
                print(data)
                print(response.text)

        try:
            responseJson = response.json()
        except:
            raise ServerError({"error": True, "errMsg": response.text})

        return {"data": responseJson}
    # Functons to handle Cable Requests

    def service_providers(self):
        endpoint = self._baseUrl + self._endPoint['cable_tv']['list_providers']

        method = 'GET'

        return self._handleDataBundleRequests(endpoint, method, data=None)

    def multichoice_list(self, details):
        endpoint = self._baseUrl + \
            self._endPoint['cable_tv']['multichoice_list']
        data = details

        # Parse url to include details
        url_parts = list(urlparse.urlparse(endpoint))
        query = dict(urlparse.parse_qsl(url_parts[4]))
        query.update(details)
        url_parts[4] = urlencode(query)
        endpoint = urlparse.urlunparse(url_parts)

        method = 'POST'

        return self._handleCableTvRequests(endpoint, method, data=data)

    def multichoice_addons(self, details):
        endpoint = self._baseUrl + \
            self._endPoint['cable_tv']['multichoice_addons']
        data = details

        # Parse url to include details
        url_parts = list(urlparse.urlparse(endpoint))
        query = dict(urlparse.parse_qsl(url_parts[4]))
        query.update(details)
        url_parts[4] = urlencode(query)
        endpoint = urlparse.urlunparse(url_parts)

        method = 'POST'

        return self._handleCableTvRequests(endpoint, method, data=data)

    def request_cable_tv(self, details):
        endpt = 'https://api.staging.baxibap.com/services/multichoice/request'
        data = details

        # Parse url to include details
        # url_parts = list(urlparse.urlparse(endpt))
        # query = dict(urlparse.parse_qsl(url_parts[4]))
        # query.update(details)
        # url_parts[4] = urlencode(query)
        # endpoint = urlparse.urlunparse(url_parts)

        method = 'POST'
        return self._handleCableTvRequests(endpt, method, data=data)
