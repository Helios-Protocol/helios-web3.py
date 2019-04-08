import time

from eth_account import Account as EthAccount
from eth_utils.curried import (
    combomethod,
    keccak,
)

from collections import (
    Mapping,
)

from cytoolz import (
    dissoc,
)
from eth_keys.datatypes import PrivateKey

from typing import (
    Tuple,
    List,
)

from hvm.vm.forks.helios_testnet.transactions import HeliosTestnetTransaction
# fields = [
#         ('nonce', big_endian_int),
#         ('gas_price', big_endian_int),
#         ('gas', big_endian_int),
#         ('to', address),
#         ('value', big_endian_int),
#         ('data', binary),
#         ('v', big_endian_int),
#         ('r', big_endian_int),
#         ('s', big_endian_int),
#     ]

from hvm.vm.forks.helios_testnet.transactions import HeliosTestnetReceiveTransaction
# fields = [
#         ('sender_block_hash', hash32),
#         ('send_transaction_hash', hash32),
#         ('is_refund', boolean),
#         ('remaining_refund', big_endian_int)
#     ]

from hvm.vm.forks.helios_testnet.blocks import HeliosTestnetBlock

from hvm.db.trie import make_trie_root_and_nodes

from hvm.rlp.headers import (
    MicroBlockHeader,
    BlockHeader)

# fields = [
#     ('chain_address', address),
#     ('parent_hash', hash32),
#     ('transaction_root', trie_root),
#     ('receive_transaction_root', trie_root),
#     ('block_number', big_endian_int),
#     ('timestamp', big_endian_int),
#     ('extra_data', binary),
#     ('reward_hash', hash32),
#     ('v', big_endian_int),
#     ('r', big_endian_int),
#     ('s', big_endian_int),
# ]



class Account(EthAccount):

    @combomethod
    def signBlock(self, send_transaction_dicts: List[dict], receive_transaction_dicts: List[dict], header_dict: dict, private_key) -> Tuple[bytes]:
        '''

        transaction = {
                    # Note that the address must be in checksum format:
                    'to': '0xF0109fC8DF283027b6285cc889F5aA624EaC1F55',
                    'value': 1000000000,
                    'gas': 2000000,
                    'gasPrice': 234567897654321,
                    'nonce': 0,
                    'chainId': 1
                }

         receive_transaction = {
                'senderBlockHash',
                'sendTransactionHash',
                'isRefund',
                'remainingRefund'
            }

        header = {
                'parentHash',
                'blockNumber',
                'extraData',
            }

        :param send_transaction_dicts:
        :param receive_transaction_dicts:
        :param reward_bundle:
        :param private_key:
        :return:
        '''

        account = self.privateKeyToAccount(private_key)
        chain_id = 1
        send_transactions = []
        for transaction_dict in send_transaction_dicts:
            tx = HeliosTestnetTransaction(nonce = transaction_dict.nonce,
                                          gas_price = transaction_dict.gasPrice,
                                          gas = transaction_dict.gas,
                                          to = transaction_dict.to,
                                          value = transaction_dict.value,
                                          )
            chain_id = transaction_dict.chainId
            signed_tx = tx.get_signed(account._key_obj, chain_id)
            send_transactions.append(signed_tx)

        receive_transactions = []
        for receive_transaction_dict in receive_transaction_dicts:
            tx = HeliosTestnetReceiveTransaction(sender_block_hash = receive_transaction_dict.senderBlockHash,
                                                 send_transaction_hash = receive_transaction_dict.sendTransactionHash,
                                                 is_refund = receive_transaction_dict.isRefund,
                                                 remaining_refund = receive_transaction_dict.remainingRefund)
            receive_transactions.append(tx)


        send_tx_root_hash, _ = make_trie_root_and_nodes(send_transactions)
        receive_tx_root_hash, _ = make_trie_root_and_nodes(receive_transactions)

        chain_address = account.address

        timestamp = int(time.time())

        header = BlockHeader(chain_address = chain_address,
                              parent_hash = header_dict.parentHash,
                              transaction_root = send_tx_root_hash,
                              receive_transaction_root = receive_tx_root_hash,
                              block_number = header_dict.blockNumber,
                              timestamp = timestamp,
                              extra_data = header_dict.extraData)

        signed_header = header.get_signed(account._key_obj, chain_id)

