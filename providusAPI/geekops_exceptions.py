class geekopsExceptions(Exception):
    def __init__(self,msg):
        """This is an error relating to one of the functions in geekops"""
        super(BremitExceptions, self).__init__(msg)
        pass


class ServerError(geeopsExceptions):

    """Raised when a server error is encountered"""

    def __init__(self, err):
        self.err = err

    def __str__(self):
        return "Transaction Query Failed with message" + self.err['errMsg']


class AccountError(geekopsExceptions):
    """Raised during pre authentiction of user credentials"""

    def __init__(self, err):
        self.err = err

    def __str__(self):
        return "Account details Query Failed with message"+self.err['errMsg']


class TransferError(geekopsExceptions):
    """Raised when there is a failed transaction"""

    def __init__(self, err):
        self.err = err

    def __str__(self):
        return "Account details Query Failed with message"+self.err['errMsg']
