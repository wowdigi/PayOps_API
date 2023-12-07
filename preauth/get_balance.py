import requests
import json


def balance(user_url):
    """This module validates a users wallet balance to know if they are eligible to carry out transactions"""
    headers = {
        'content-type': 'application/json',
        'accept': 'application/json',
    }

    endpoint = user_url

    response = requests.get(url=endpoint, headers=headers)

    try:
        responseJson = response.json()['account_balance']
    except:
        return 'The Request didnt return a Json Response'

    if response.ok:
        return responseJson
