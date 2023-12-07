class geekopsError(Exception):
    def __init__(self, msg):
        """This is an error relating to one of the functions in geekops"""
        super(geekopsError, self).__init__(msg)
        pass


class TransactionError(geekopsError):
    """Raised when querying of a transaction failed"""

    def __init__(self, err):
        self.err = err

    def __str__(self):
        return "Transaction Query Failed with message"+self.err['errMsg']


class ParameterError(geekopsError):
    """Raised when Parameter supplied is Invalid"""

    def __init__(self, err):
        self.err = err

    def __str__(self):
        return "Transaction Request Failed with message"+self.err['errMsg']


class AgentError(geekopsError):
    """Raised when Agent being looked up doesnt exist"""

    def __init__(self, err):
        self.err = err

    def __str__(self):
        return "Agent Query Failed with message"+self.err['errMsg']


class BillerError(geekopsError):
    """Raised when requested biller service doesnt exist"""

    def __init__(self, err):
        self.err = err

    def __str__(self):
        return "Biller Query Failed with message"+self.err['errMsg']


class AccountError(geekopsError):
    """Raised during pre authentiction of user credentials"""

    def __init__(self, err):
        self.err = err

    def __str__(self):
        return "Account details Query Failed with message"+self.err['errMsg']


class AirtimeProviderError(geekopsError):
    """Raised when airtime provider requested doesnt exist"""

    def __init__(self, err):
        self.err = err

    def __str__(self):
        return "Airtime Provider Request Failed with message"+self.err['errMsg']


class AirtimeRequestError(geekopsError):
    """Raised when Airtime Request Fails"""

    def __init__(self, err):
        self.err = err

    def __str__(self):
        return "Airtime Request Failed with message"+self.err['errMsg']


class ServerError(geekopsError):
    """ Raised when the server is down or when it could not process your request """

    def __init__(self, err):
        self.err = err

    def __str__(self):
        return " Server is down with error: " + self.err["errMsg"]
