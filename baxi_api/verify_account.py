import requests
import json
import urllib.parse as urlparse
from urllib.parse import urlencode
from .geekops_exceptions import AgentError, ServerError, TransactionError, BillerError
from .geekops_base import geekopsBase


class VerifyAccount(geekopsBase):
    """
    Class to handle pre-authentication process.
    Verifies if account_number of user exists
    """

    def __init__(self, apiKey):
        self.headers = {
            'content-type': 'application/json',
            'authorization': 'Api-key 9e6936-4e7616-d45829-e4ee98-66278f',
            'accept': 'application/json',
        }
        super(VerifyAccount, self).__init__(apiKey)

    def _preliminaryResponseChecks(self, response, TypeOfErrorToRaise, name):

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

    def _handleAccountVerification(self, endpoint, method, data=None):
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

    def get_service(self, service_type, account_number):
        endpt = self._baseUrl + \
            self._endPoint['preauth']['verify_account']
        data = {**service_type, **account_number}

        # Parse url to include service_type
        # url_parts = list(urlparse.urlparse(endpt))
        # query = dict(urlparse.parse_qsl(url_parts[4]))
        # query.update(data)
        # url_parts[4] = urlencode(query)
        # endpoint = urlparse.urlunparse(url_parts)

        method = 'POST'

        return self._handleAccountVerification(endpt, method, data=data)
