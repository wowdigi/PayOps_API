import requests
import json
import urllib.parse as urlparse
from urllib.parse import urlencode
from .geekops_exceptions import AgentError, ServerError, TransactionError, BillerError
from .geekops_base import geekopsBase


class Billers(geekopsBase):
    """Class to handle billers Transactions
        1.Providers List
        2.Service List
        3.Category List
        4.Service based on Category
    """

    def __init__(self, apiKey):
        self.headers = {
            'content-type': 'application/json',
            'x-api-key': 'apikey',
            'accept': 'application/json',
        }
        super(Billers, self).__init__(apiKey)

    def _preliminaryResponseChecks(self, response, TypeOfErrorToRaise, name):
        # check if we can get json

        try:
            responseJson = response.json()
        except:
            raise ServerError(
                {"error": True, 'name': name, 'errMsg': response})

        # check for data parameter in response
        if not responseJson.get('data', None):
            raise TypeOfErrorToRaise(
                {"error": True, 'name': name, 'errMsg': responseJson.get('message', 'Server is Down')})

        if not response.ok:
            errMsg = response.get('message', None)
            raise TypeOfErrorToRaise({"error": True, "errMsg": errMsg})

        return responseJson

    def _handleBillerRequests(self, endpoint, method, data=None):
        # check response method
        if method == 'GET':
            if data == None:
                response = requests.get(endpoint, headers=self.headers)
            else:
                response = requests.get(
                    endpoint, headers=self.headers, data=json.dumps(data))

        elif method == 'POST':
            if data == None:
                response = requests.post(endpoint, headers=self.headers)

            else:
                response = requests.post(
                    endpoint, headers=self.headers, data=json.dumps(data))

        try:
            responseJson = response.json()
        except:
            raise ServerError({"error": True, "errMsg": response.text})

        if response.ok:
            return {"error": False, "data": responseJson}
        else:
            {"error": True, "data": responseJson}
    # function to get biller details

    def all_billers(self):
        endpoint = self._baseUrl + self._endPoint['billers']['list_providers']

        method = 'GET'

        return self._handleBillerRequests(endpoint, method, data=None)

    def service_providers(self):
        endpoint = self._baseUrl + self._endPoint['billers']['list_services']

        method = 'GET'

        return self._handleBillerRequests(endpoint, method, data=None)

    def all_category(self):
        endpoint = self._baseUrl + self._endPoint['billers']['list_category']

        method = "GET"

        return self._handleBillerRequests(endpoint, method, data=None)

    def service_category(self, service_type):
        endpt = self._baseUrl + \
            self._endPoint['billers']['service_in_category']
        data = service_type

        # Parse url to include service_type
        # url_parts = list(urlparse.urlparse(endpt))
        # query = dict(urlparse.parse_qsl(url_parts[4]))
        # query.update(service_type)
        # url_parts[4] = urlencode(query)
        # endpoint = urlparse.urlunparse(url_parts)

        method = 'POST'
        return self._handleBillerRequests(endpt, method, data=data)
