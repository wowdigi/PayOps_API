import requests
import json
import urllib.parse as urlparse
from urllib.parse import urlencode
from .geekops_exceptions import AgentError, ServerError, TransactionError, AccountError
from .geekops_base import geekopsBase


class AgentTransaction(geekopsBase):
    def __init__(self, apiKey):
        super(AgentTransaction, self).__init__(apiKey)

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

    def _handleAgentStatusRequest(self, endpoint, method='GET', data=None):
        # request Headers
        headers = {
            'content-type': 'application/json',
            'authorization': 'Api-key c0a111-28a93e-6490ab-3a77f3-e27227',
            'accept': 'application/json',
        }

        if method:
            if data == None:
                response = requests.get(endpoint, headers=headers)
            else:
                response = requests.get(
                    endpoint, headers=headers, data=json.dumps(data))
        try:
            responseJson = response.json()

        except:
            raise ServerError({"error": True, "errMsg": response.text})

        if response.ok:
            return {'error': False, 'data': responseJson}
        else:
            return AgentError({'error': False, 'data': responseJson})

    def transaction(self, details):
        endpt = self._baseUrl + self._endPoint["superagent"]["requery"] + "?"
        data = details

        # parse query params
        url_parts = list(urlparse.urlparse(endpt))
        query = dict(urlparse.parse_qsl(url_parts[4]))
        query.update(details)
        url_parts[4] = urlencode(query)
        endpoint = urlparse.urlunparse(url_parts)

        method = 'GET'

        return self._handleAgentStatusRequest(endpoint, method, data=data)

    def retry_transaction(self, details):
        endpt = self._baseUrl + self._endPoint["superagent"]["retry"] + "?"
        data = details

        # parse query params
        url_parts = list(urlparse.urlparse(endpt))
        query = dict(urlparse.parse_qsl(url_parts[4]))
        query.update(details)
        url_parts[4] = urlencode(query)
        endpoint = urlparse.urlunparse(url_parts)

        method = 'GET'

        return self._handleAgentStatusRequest(endpoint, method, data=data)

    def agent_balance(self):
        endpt = self._baseUrl + self._endPoint["superagent"]["agent_balance"]

        # parse query params
        url_parts = list(urlparse.urlparse(endpt))
        query = dict(urlparse.parse_qsl(url_parts[4]))
        url_parts[4] = urlencode(query)
        endpoint = urlparse.urlunparse(url_parts)

        method = 'GET'

        return self._handleAgentStatusRequest(endpoint, method)

    def refresh(self):
        endpt = self._baseUrl + self._endPoint["superagent"]["agent_balance"]

        # parse query params
        # url_parts = list(urlparse.urlparse(endpt))
        # query = dict(urlparse.parse_qsl(url_parts[4]))
        # url_parts[4] = urlencode(query)
        # endpoint = urlparse.urlunparse(url_parts)

        method = 'GET'

        return self._handleAgentStatusRequest(endpt, method)
