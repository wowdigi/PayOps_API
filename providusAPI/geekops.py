from .geekops_api import NipTransfer

class Remit:

    def __init__(self):
        """
        This is main organizing object. It contains the following:
        bremit.NIPTransfers
        """

        self.NipTransfer = NipTransfer()