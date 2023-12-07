class Bremit(object):
    """
    Base class for geekopss Providus Bank Endpoint.
    This class contains endpoints as Attributes
    """

    def __init__(self):
        self._baseUrl = 'http://192.168.156.27:8888/postingrest/'
        self._urlEndpoint = {
            'bvndetails': 'GetBvnDetails/',
            'accountdetails': 'GetNIPAccount/',
            'transfer': 'NIPFundTransfer/',
            'banks': 'GetNIPBanks/',
            'providusbalance': 'GetProvidusAccount/',
            'status': 'GetNIPTransactionStatus/',


        }
