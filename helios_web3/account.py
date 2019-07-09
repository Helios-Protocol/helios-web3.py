import time

from eth_account import Account as EthAccount
from eth_utils.curried import (
    combomethod,
    keccak,
    encode_hex,
    decode_hex
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
import rlp_cython as rlp
from hvm.vm.forks.boson.transactions import BosonTransaction
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

from hvm.vm.forks.boson.transactions import BosonReceiveTransaction
# fields = [
#         ('sender_block_hash', hash32),
#         ('send_transaction_hash', hash32),
#         ('is_refund', boolean),
#         ('remaining_refund', big_endian_int)
#     ]

from hvm.vm.forks.boson import BosonMicroBlock

# fields = [
#     ('header', MicroBlockHeader),
#     ('transactions', CountableList(BosonTransaction)),
#     ('receive_transactions', CountableList(BosonReceiveTransaction)),
#     ('reward_bundle', StakeRewardBundle),
# ]

from hvm.rlp.headers import MicroBlockHeader

from hvm.utils.rlp import convert_rlp_to_correct_class

from hvm.db.trie import make_trie_root_and_nodes

from hvm.rlp.headers import (
    MicroBlockHeader,
    BlockHeader)

from eth_account.datastructures import (
    AttributeDict,
)

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
from hvm.rlp.consensus import StakeRewardBundle


class Account(EthAccount):

    @combomethod
    def signBlock(self, header_dict: dict, private_key: str, send_transaction_dicts: List[dict] = [], receive_transaction_dicts: List[dict] = [] ) -> AttributeDict:
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

        if "extraData" in header_dict:
            extra_data = header_dict['extraData']
        else:
            extra_data = b''

        if "chainId" in header_dict:
            chain_id = header_dict['chainId']
        else:
            chain_id = 1
        account = self.privateKeyToAccount(private_key)

        send_transactions = []
        for transaction_dict in send_transaction_dicts:
            tx = BosonTransaction(nonce = transaction_dict['nonce'],
                                          gas_price = transaction_dict['gasPrice'],
                                          gas = transaction_dict['gas'],
                                          to = transaction_dict['to'],
                                          value = transaction_dict['value'],
                                          data = transaction_dict['data'] if 'data' in transaction_dict else b'',
                                          v = 0,
                                          r = 0,
                                          s = 0
                                          )
            signed_tx = tx.get_signed(account._key_obj, chain_id)
            send_transactions.append(signed_tx)

        receive_transactions = []
        for receive_transaction_dict in receive_transaction_dicts:
            tx = BosonReceiveTransaction(sender_block_hash = receive_transaction_dict['senderBlockHash'],
                                                 send_transaction_hash = receive_transaction_dict['sendTransactionHash'],
                                                 is_refund = receive_transaction_dict['isRefund'],
                                                 remaining_refund = receive_transaction_dict['remainingRefund'])
            receive_transactions.append(tx)


        send_tx_root_hash, _ = make_trie_root_and_nodes(send_transactions)
        receive_tx_root_hash, _ = make_trie_root_and_nodes(receive_transactions)

        chain_address = account.address

        timestamp = int(time.time())

        header = BlockHeader(chain_address = decode_hex(chain_address),
                              parent_hash = header_dict['parentHash'],
                              transaction_root = send_tx_root_hash,
                              receive_transaction_root = receive_tx_root_hash,
                              block_number = header_dict['blockNumber'],
                              timestamp = timestamp,
                              extra_data = extra_data)

        signed_header = header.get_signed(account._key_obj, chain_id)
        signed_micro_header = signed_header.to_micro_header()

        micro_block = BosonMicroBlock(header = signed_micro_header,
                                      transactions = send_transactions,
                                      receive_transactions = receive_transactions,
                                      reward_bundle = StakeRewardBundle())

        rlp_encoded_micro_block = rlp.encode(micro_block, sedes=BosonMicroBlock)

        return AttributeDict({
            'rawBlock': encode_hex(rlp_encoded_micro_block),
            'hash': encode_hex(signed_header.micro_header_hash),
            'r': signed_header.r,
            's': signed_header.s,
            'v': signed_header.v,
        })

