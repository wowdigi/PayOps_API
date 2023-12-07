

class geekopsBase(object):
    """ This is the core of the implementation. It contains the encryption and initialization functions.
    def __init__(self,apiKey)"""

    def __init__(self, apiKey=None):
        self._apiKey = apiKey
        self._baseUrl = "https://api.staging.baxibap.com"
        self._endPoint = {
            "superagent": {

                "requery": "/superagent/transaction/requery",
                "retry": '/superagent/transaction/retry',
                "agent_balance": "/superagent/account/balance",
                "refresh": "/superagent/services/refresh",

            },
            "billers": {
                "list_providers": "/billers/providers/list",
                "list_services": "/billers/services/list",
                "list_category": "/billers/category/all",
                "service_in_category": "/billers/services/category",

            },
            "preauth": {

                "verify_account": "/services/namefinder/query",

            },
            "airtime": {

                "list_providers": "/services/airtime/providers",
                "request": "/services/airtime/request"

            },
            "data_bundles": {

                "list_providers": "/services/databundle/providers",
                "list_data_bundles": "/services/databundle/bundles",
                "data_bundles_request": "/services/databundle/request",

            },
            "cable_tv": {
                "list_providers": "/services/cabletv/providers",
                "multichoice_list": "​/services​/multichoice​/list",
                "multichoice_addons": "​/services​/multichoice​/addons",
                "cable_tv_request": "​/services/multichoice/request",

            },
            "electricity": {

                "electricity_billers": "​/services​/electricity​/billers",
                "verify_user": "/services/electricity/verify",
                "electricity_request": "/services/electricity/request"

            }

        }

    def _getApiKey(self):
        return self._apiKey
