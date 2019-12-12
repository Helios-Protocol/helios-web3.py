
from typing import (
    Tuple,
    List,
    Dict, Any)

from eth_utils import to_wei
from hvm.constants import GAS_TX
from eth_keys.datatypes import PrivateKey

def prepare_and_sign_block(w3, private_key: PrivateKey, transactions: List[Dict[str, Any]]):
    block_creation_parameters = w3.hls.getBlockCreationParams(private_key.public_key.to_canonical_address())

    header_dict = {'blockNumber': block_creation_parameters['block_number'],
                   'parentHash': block_creation_parameters['parent_hash']}

    #
    # Prepare transactions
    #

    nonce = block_creation_parameters['nonce']
    min_gas_price = w3.hls.gasPrice
    min_gas_price = min_gas_price + 1
    gas_price = to_wei(min_gas_price, 'gwei')

    for i in range(len(transactions)):
        if 'gas' not in transactions[i]:
            transactions[i]['gas'] = GAS_TX
        transactions[i]['nonce'] = nonce
        transactions[i]['gasPrice'] = gas_price

        nonce = nonce + 1

    signed_block = w3.hls.account.signBlock(send_transaction_dicts=transactions,
                                                 header_dict=header_dict,
                                                 private_key=str(private_key))

    return signed_block, header_dict, transactions