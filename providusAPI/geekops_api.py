import requests
import json
import urllib.parse as urlparse
from urllib.parse import urlencode
from .bremit_exceptions import ServerError, TransferError, AccountError
from .bremit_base import Bremit


class NipTransfer(Bremit):
    def __init__(self):
        super(NipTransfer, self).__init__()

    def _checkresponsedata(self, response, TypeOfErrorToRaise, reference):
        # check if we got a json response
        try:
            responseJson = response.json()
        except:
            raise ServerError(
                {"error": True, 'reference': reference, "errMsg": response})

        if not responseJson.get('data', None):
            raise TypeOfErrorToRaise(
                {'error': True, "reference": reference, 'errMsg': responseJson.get('data', "Server is down")})

        if not response.ok:
            errMsg = responseJson['data'].get('message', None)

        return responseJson

    def _handleAgentStatusRequest(self, endpoint, method, data=None):
        # request Headers
        headers = {
            'content-type': 'application/json',
            'accept': 'application/json',
        }

        if method == 'GET':
            if data == None:
                response = requests.get(url=endpoint, headers=headers)
            else:
                response = requests.get(
                    url=endpoint, headers=headers, data=json.dumps(data))

        elif method == 'POST':
            if data == None:
                response = requests.post(
                    url=endpoint, headers=headers, timeout=25)

            else:
                response = requests.post(
                    url=endpoint, headers=headers, json=data, timeout=25)
        try:
            responseJson = response.json()

        except:
            raise ServerError({"error": True, "errMsg": response.text})

        if response.ok:
            return {'error': False, 'data': responseJson}
        else:
            return ServerError({'error': False, 'data': responseJson})

    def getProvidusAccount(self, details):
        endpt = self._baseUrl + self._urlEndpoint["providusbalance"]
        data = details

        # parse query params
        url_parts = list(urlparse.urlparse(endpt))
        query = dict(urlparse.parse_qsl(url_parts[4]))
        query.update(details)
        url_parts[4] = urlencode(query)
        endpoint = urlparse.urlunparse(url_parts)

        method = 'POST'

        return self._handleAgentStatusRequest(endpoint, method, data=data)

    def getNipBanks(self):
        endpoint = self._baseUrl + self._urlEndpoint["banks"]

        method = 'GET'

        return self._handleAgentStatusRequest(endpoint, method)

    def getNipAccount(self, details):
        endpt = self._baseUrl + self._urlEndpoint["accountdetails"]

        # parse query params
        data = details

        # Parse url to include details
        # url_parts = list(urlparse.urlparse(endpt))
        # query = dict(urlparse.parse_qsl(url_parts[4]))
        # query.update(details)
        # url_parts[4] = urlencode(query)
        # endpoint = urlparse.urlunparse(url_parts)

        method = 'POST'

        return self._handleAgentStatusRequest(endpt, method, data=data)

    def nipFundTransfer(self, details):
        endpt = self._baseUrl + self._urlEndpoint["transfer"]

        # parse query params
        data = details

        # Parse url to include details
        # url_parts = list(urlparse.urlparse(endpt))
        # query = dict(urlparse.parse_qsl(url_parts[4]))
        # query.update(details)
        # url_parts[4] = urlencode(query)
        # endpoint = urlparse.urlunparse(url_parts)
        method = 'POST'

        return self._handleAgentStatusRequest(endpt, method, data=data)

    def getNIPTransactionStatus(self, details):

        endpt = self._baseUrl + self._urlEndpoint["status"]

        # parse query params
        data = details

        # Parse url to include details
        url_parts = list(urlparse.urlparse(endpt))
        query = dict(urlparse.parse_qsl(url_parts[4]))
        query.update(details)
        url_parts[4] = urlencode(query)
        endpoint = urlparse.urlunparse(url_parts)

        method = 'POST'

        return self._handleAgentStatusRequest(endpoint, method, data=data)

    def getBvnDetails(self):

        endpt = self._baseUrl + self._urlEndpoint["bvndetails"]

        # parse query params
        url_parts = list(urlparse.urlparse(endpt))
        query = dict(urlparse.parse_qsl(url_parts[4]))
        url_parts[4] = urlencode(query)
        endpoint = urlparse.urlunparse(url_parts)

        method = 'POST'

        return self._handleAgentStatusRequest(endpoint, method)
