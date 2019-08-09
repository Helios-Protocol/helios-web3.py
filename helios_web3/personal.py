from web3.geth import GethPersonal
from web3.method import (
    Method,
    default_root_munger,
)

class Personal(GethPersonal):
    '''
    Class to allow for overriding functions if necessary
    '''
    sendTransactions = Method(
        "personal_sendTransactions",
        mungers=[default_root_munger],
    )

    receiveTransactions = Method(
        "personal_receiveTransactions",
        mungers=[default_root_munger],
    )

    getAccountsWithReceivableTransactions = Method(
        "personal_getAccountsWithReceivableTransactions",
        mungers=[default_root_munger],
    )

