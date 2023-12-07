import requests
import json


def authenticate_balance(user_url, transaction_amount, apikey=None):
    """This module validates a users wallet balance to know if they are eligible to carry out transactions"""
    headers = {
        'content-type': 'application/json',
        'accept': 'application/json',
    }

    if apikey:
        headers['authorization'] = 'Api_key api-key'
        

    endpoint = user_url

    response = requests.get(url=endpoint, headers=headers)

    try:
        responseJson = response.json()
    except:
        return 'The Request didnt return a Json Response'

    if response.ok:
        balance = float(responseJson['account_balance'])
        print(balance)
        transaction_amount = float(transaction_amount)
        if balance > transaction_amount:
            return True

        else:
            return False
