
from baxi_api.geekops_airtime import Airtime
from baxi_api.geekops_base import geekopsBase
from baxi_api.billers import Billers
from baxi_api.transactions import AgentTransaction
from baxi_api.verify_account import VerifyAccount
from .geekops_airtime import Airtime
from .geekops_data_bundles import DataBundles
from .geekops_cable_tv import CableTv
from .geekops_electricity import Electricity
from .billers import Billers
from .transactions import AgentTransaction
from .verify_account import VerifyAccount


class geekops:

    def __init__(self, apiKey):
        """
        This is main organizing object. It contains the following:\n
        geekops.Airtime -- For Airtime Transactions\n
        geekops.DataBundles -- For Data Bundles Transactions\n
        geekops.CableTv -- For Cable Tv Transactions\n
        geekops.Electricity -- For Electrcity Transactions\n
        geekops.Billers -- For TV subscription \n
        geekops.VerifyAccount -- Preauth class to verify account details before transaction\n
        geekops.AgentTransaction -- for super users to carry out agent transactions\n
        """

        self.Airtime = Airtime(apiKey)
        self.DataBundles = DataBundles(apiKey)
        self.CableTv = CableTv(apiKey)
        self.Electricity = Electricity(apiKey)
        self.Billers = Billers(apiKey)
        self.AgentTransaction = AgentTransaction(apiKey)
        self.VerifyAccount = VerifyAccount(apiKey)
