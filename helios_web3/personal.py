from web3.geth import GethPersonal
from web3.method import (
    Method,
    default_root_munger,
)

def unlock_account_munger(module, wallet_address, password, duration = 300):
    return [wallet_address, password, duration]

def get_accounts_with_receivable_transactions_munger(module, after_timestamp=0):
    return [after_timestamp]

class Personal(GethPersonal):
    '''
    Class to allow for overriding functions if necessary
    '''

    sendTransactions = Method(
        "personal_sendTransactions",
        mungers=[default_root_munger],
    )


    unlockAccount = Method(
        "personal_unlockAccount",
        mungers=[unlock_account_munger],
    )

    receiveTransactions = Method(
        "personal_receiveTransactions",
        mungers=[default_root_munger],
    )

    getAccountsWithReceivableTransactions = Method(
        "personal_getAccountsWithReceivableTransactions",
        mungers=[get_accounts_with_receivable_transactions_munger],
    )

