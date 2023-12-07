import requests
import json


class Capricorn(object):
    def __init__(self,apiKey):
        self._baseUrl = 'https://api.staging.baxibap.com/'
        self._headers = {
            "Content-Type":"application/json",
            "Accept":"application/json",
            "x-api-key":apiKey,
        }
        self._endpoints = {
            'airtime_providers':'',
            'purchase_airtime':'',
            'get_databundle_package':'',
            'purchase_databundle':'',
            'purchase_electricity':'',
            'purchase_tvsub':'',
        }

    def _getObject(self,method,url,payload):
        payload = json.dumps(payload)
        response = requests.request(
            method=method,
            url=url,
            data=payload
        )

        if response.status_code == 200 and response.json():
            responseObject = response.json()['data']

        return responseObject

    def _handleResponseObject(self,response):
        data = response['data']
        return data

 
    def _getAirtimeProviders(self,payload):
        url = self._baseUrl + self._endpoints['airtime_providers']
        res = self._getObject('GET',url,payload)



    def _purchaseAirtime(self,payload):
        url = self._baseUrl + self._endpoints['purchase_airtime']
        res = self._getObject('POST',url,payload)
        if res['statusCode'] == '0':
            airtime_response = {
                'message':res['provider_message'],
                'reference':res['transactionReference']
            }

            return airtime_response

    def _getDataBundleProviders(self,payload):
        url = self._baseUrl + self._endpoints['get_databundle_package']
        res = self._getObject('POST',url,payload)
        databundle = []
        for bundle in res:
            databundle.append(
                {
                    "name":bundle["name"],
                    "price":bundle["price"],
                    "datacode": bundle["datacode"]
                }
            )

        return databundle

    def _purchaseDataBundle(self,payload):
        url = self._baseUrl + self._endpoints['purchase_databundle']
        res = self._getObject('POST',url,payload)
        if res['statusCode'] == '0':
            databundle_response = {
                "reference":res["transactionReference"],
                "message":res["transactionMessage"],

            }

            return databundle_response



    def _purchaseElectricity(self,payload):
        url = self._baseUrl + self._endpoints['purchase_airtime']
        res = self._getObject('POST',url,payload)


    def _cableNameValidation(self,payload):
        url = self._baseUrl + self._endpoints['cable_name_validation']
        res = self._getObject('POST',url,payload)
        
    
    def _purchaseTvSubscription(self,payload):
        url = self._baseUrl + self._endpoints['purchase_tvsub']
        res = self._getObject('POST',url,payload)
