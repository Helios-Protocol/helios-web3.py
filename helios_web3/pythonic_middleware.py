import codecs
import operator

from eth_utils.curried import (
    apply_formatters_to_sequence,
    is_address,
    is_bytes,
    is_integer,
    is_null,
    is_string,
    remove_0x_prefix,
    text_if_str,
    to_checksum_address,
)
from eth_utils.toolz import (
    complement,
    compose,
    curried,
    curry,
    partial,
)
from hexbytes import (
    HexBytes,
)

from web3._utils.abi import (
    is_length,
)
from web3._utils.encoding import (
    hexstr_if_str,
    to_hex,
    to_text
)
from web3._utils.formatters import (
    apply_formatter_at_index,
    apply_formatter_if,
    apply_formatter_to_array,
    apply_formatters_to_dict,
    apply_one_of_formatters,
    hex_to_integer,
    integer_to_hex,
    is_array_of_dicts,
    is_array_of_strings,
    remove_key_if,
)

from web3.middleware.formatting import (
    construct_formatting_middleware,
)


def bytes_to_ascii(value):
    return codecs.decode(value, 'ascii')


to_ascii_if_bytes = apply_formatter_if(is_bytes, bytes_to_ascii)
to_integer_if_hex = apply_formatter_if(is_string, hex_to_integer)
block_number_formatter = apply_formatter_if(is_integer, integer_to_hex)


is_false = partial(operator.is_, False)

is_not_false = complement(is_false)
is_not_null = complement(is_null)


@curry
def to_hexbytes(num_bytes, val, variable_length=False):
    if isinstance(val, (str, int, bytes)):
        result = HexBytes(val)
    else:
        raise TypeError("Cannot convert %r to HexBytes" % val)

    extra_bytes = len(result) - num_bytes
    if extra_bytes == 0 or (variable_length and extra_bytes < 0):
        return result
    elif all(byte == 0 for byte in result[:extra_bytes]):
        return HexBytes(result[extra_bytes:])
    else:
        raise ValueError(
            "The value %r is %d bytes, but should be %d" % (
                result, len(result), num_bytes
            )
        )


TRANSACTION_FORMATTERS = {
    'blockHash': apply_formatter_if(is_not_null, to_hexbytes(32)),
    'blockNumber': apply_formatter_if(is_not_null, to_integer_if_hex),
    'transactionIndex': apply_formatter_if(is_not_null, to_integer_if_hex),
    'nonce': to_integer_if_hex,
    'gas': to_integer_if_hex,
    'gasPrice': to_integer_if_hex,
    'value': to_integer_if_hex,
    'from': to_checksum_address,
    'publicKey': apply_formatter_if(is_not_null, to_hexbytes(64)),
    'r': to_hexbytes(32, variable_length=True),
    'raw': HexBytes,
    's': to_hexbytes(32, variable_length=True),
    'to': apply_formatter_if(is_address, to_checksum_address),
    'hash': to_hexbytes(32),
    'v': apply_formatter_if(is_not_null, to_integer_if_hex),
    'standardV': apply_formatter_if(is_not_null, to_integer_if_hex),
}


transaction_formatter = apply_formatters_to_dict(TRANSACTION_FORMATTERS)


SIGNED_TX_FORMATTER = {
    'raw': HexBytes,
    'tx': transaction_formatter,
}


signed_tx_formatter = apply_formatters_to_dict(SIGNED_TX_FORMATTER)


WHISPER_LOG_FORMATTERS = {
    'sig': to_hexbytes(130),
    'topic': to_hexbytes(8),
    'payload': HexBytes,
    'padding': apply_formatter_if(is_not_null, HexBytes),
    'hash': to_hexbytes(64),
    'recipientPublicKey': apply_formatter_if(is_not_null, to_hexbytes(130)),
}


whisper_log_formatter = apply_formatters_to_dict(WHISPER_LOG_FORMATTERS)


LOG_ENTRY_FORMATTERS = {
    'blockHash': apply_formatter_if(is_not_null, to_hexbytes(32)),
    'blockNumber': apply_formatter_if(is_not_null, to_integer_if_hex),
    'transactionIndex': apply_formatter_if(is_not_null, to_integer_if_hex),
    'transactionHash': apply_formatter_if(is_not_null, to_hexbytes(32)),
    'logIndex': to_integer_if_hex,
    'address': to_checksum_address,
    'topics': apply_formatter_to_array(to_hexbytes(32)),
    'data': to_ascii_if_bytes,
}


log_entry_formatter = apply_formatters_to_dict(LOG_ENTRY_FORMATTERS)


RECEIPT_FORMATTERS = {
    'blockHash': apply_formatter_if(is_not_null, to_hexbytes(32)),
    'blockNumber': apply_formatter_if(is_not_null, to_integer_if_hex),
    'transactionIndex': apply_formatter_if(is_not_null, to_integer_if_hex),
    'transactionHash': to_hexbytes(32),
    'cumulativeGasUsed': to_integer_if_hex,
    'status': to_integer_if_hex,
    'gasUsed': to_integer_if_hex,
    'contractAddress': apply_formatter_if(is_not_null, to_checksum_address),
    'logs': apply_formatter_to_array(log_entry_formatter),
    'logsBloom': to_hexbytes(256),
}


receipt_formatter = apply_formatters_to_dict(RECEIPT_FORMATTERS)

BLOCK_FORMATTERS = {
    'extraData': to_hexbytes(32, variable_length=True),
    'gasLimit': to_integer_if_hex,
    'gasUsed': to_integer_if_hex,
    'size': to_integer_if_hex,
    'timestamp': to_integer_if_hex,
    'hash': apply_formatter_if(is_not_null, to_hexbytes(32)),
    'logsBloom': to_hexbytes(256),
    'miner': apply_formatter_if(is_not_null, to_checksum_address),
    'mixHash': to_hexbytes(32),
    'nonce': apply_formatter_if(is_not_null, to_hexbytes(8, variable_length=True)),
    'number': apply_formatter_if(is_not_null, to_integer_if_hex),
    'parentHash': apply_formatter_if(is_not_null, to_hexbytes(32)),
    'sha3Uncles': apply_formatter_if(is_not_null, to_hexbytes(32)),
    'uncles': apply_formatter_to_array(to_hexbytes(32)),
    'difficulty': to_integer_if_hex,
    'receiptsRoot': to_hexbytes(32),
    'stateRoot': to_hexbytes(32),
    'totalDifficulty': to_integer_if_hex,
    'transactions': apply_one_of_formatters((
        (apply_formatter_to_array(transaction_formatter), is_array_of_dicts),
        (apply_formatter_to_array(to_hexbytes(32)), is_array_of_strings),
    )),
    'transactionsRoot': to_hexbytes(32),
}


block_formatter = apply_formatters_to_dict(BLOCK_FORMATTERS)


STORAGE_PROOF_FORMATTERS = {
    'key': HexBytes,
    'value': HexBytes,
    'proof': apply_formatter_to_array(HexBytes),
}

ACCOUNT_PROOF_FORMATTERS = {
    'address': to_checksum_address,
    'accountProof': apply_formatter_to_array(HexBytes),
    'balance': to_integer_if_hex,
    'codeHash': to_hexbytes(32),
    'nonce': to_integer_if_hex,
    'storageHash': to_hexbytes(32),
    'storageProof': apply_formatter_to_array(apply_formatters_to_dict(STORAGE_PROOF_FORMATTERS))
}

proof_formatter = apply_formatters_to_dict(ACCOUNT_PROOF_FORMATTERS)


SYNCING_FORMATTERS = {
    'startingBlock': to_integer_if_hex,
    'currentBlock': to_integer_if_hex,
    'highestBlock': to_integer_if_hex,
    'knownStates': to_integer_if_hex,
    'pulledStates': to_integer_if_hex,
}


syncing_formatter = apply_formatters_to_dict(SYNCING_FORMATTERS)


TRANSACTION_POOL_CONTENT_FORMATTERS = {
    'pending': compose(
        curried.keymap(to_ascii_if_bytes),
        curried.valmap(transaction_formatter),
    ),
    'queued': compose(
        curried.keymap(to_ascii_if_bytes),
        curried.valmap(transaction_formatter),
    ),
}


transaction_pool_content_formatter = apply_formatters_to_dict(
    TRANSACTION_POOL_CONTENT_FORMATTERS
)


TRANSACTION_POOL_INSPECT_FORMATTERS = {
    'pending': curried.keymap(to_ascii_if_bytes),
    'queued': curried.keymap(to_ascii_if_bytes),
}


transaction_pool_inspect_formatter = apply_formatters_to_dict(
    TRANSACTION_POOL_INSPECT_FORMATTERS
)


FILTER_PARAMS_FORMATTERS = {
    'fromBlock': apply_formatter_if(is_integer, integer_to_hex),
    'toBlock': apply_formatter_if(is_integer, integer_to_hex),
}


filter_params_formatter = apply_formatters_to_dict(FILTER_PARAMS_FORMATTERS)


filter_result_formatter = apply_one_of_formatters((
    (apply_formatter_to_array(log_entry_formatter), is_array_of_dicts),
    (apply_formatter_to_array(to_hexbytes(32)), is_array_of_strings),
))

TRANSACTION_PARAM_FORMATTERS = {
    'chainId': apply_formatter_if(is_integer, str),
}


transaction_param_formatter = compose(
    remove_key_if('to', lambda txn: txn['to'] in {'', b'', None}),
    apply_formatters_to_dict(TRANSACTION_PARAM_FORMATTERS),
)

estimate_gas_without_block_id = apply_formatter_at_index(transaction_param_formatter, 0)
estimate_gas_with_block_id = apply_formatters_to_sequence([
    transaction_param_formatter,
    block_number_formatter,
])

min_gas_price_formatter = apply_formatters_to_sequence([
    to_integer_if_hex,
    to_integer_if_hex,
])


BLOCK_CREATION_PARAMETERS_FORMATTER = {
    'block_number': to_integer_if_hex,
    'parent_hash': HexBytes,
    'nonce': to_integer_if_hex,
    'receive_transactions': apply_formatter_to_array(HexBytes),
    'reward_bundle': HexBytes,
}


block_creation_parameters_formatter = apply_formatters_to_dict(BLOCK_CREATION_PARAMETERS_FORMATTER)

GET_CONNECTED_NODES_FORMATTER = {
    'url': to_text,
    'ipAddress': to_text,
    'udpPort': to_integer_if_hex,
    'tcpPort': to_integer_if_hex,
    'stake': to_integer_if_hex,
    'requestsSent': to_integer_if_hex,
    'failedRequests': to_integer_if_hex,
    'averageResponseTime': to_integer_if_hex,
}

get_connected_nodes_formatter = apply_formatters_to_dict(GET_CONNECTED_NODES_FORMATTER)

@curry
def to_hex_if_bytes(val):
    if isinstance(val, (bytes, bytearray)):
        return to_hex(val)
    else:
        return val

    
pythonic_middleware = construct_formatting_middleware(
    request_formatters={
        # Hls
        'hls_getBalance': apply_formatter_at_index(block_number_formatter, 1),
        'hls_getBlockTransactionCountByNumber': apply_formatter_at_index(
            block_number_formatter,
            0,
        ),
        'hls_getCode': apply_formatter_at_index(block_number_formatter, 1),
        'hls_getStorageAt': apply_formatter_at_index(block_number_formatter, 2),
        'hls_getTransactionCount': apply_formatter_at_index(block_number_formatter, 1),
        'hls_getBlockByNumber': apply_formatter_at_index(block_number_formatter, 0),
        'hls_getTransactionReceipt': apply_formatter_at_index(to_hex_if_bytes, 0),
        'hls_call': compose(
            apply_formatter_at_index(transaction_param_formatter, 0),
            apply_formatter_at_index(block_number_formatter, 1),
        )
        ,
    },
    result_formatters={
        # Hls
        'hls_blockNumber': to_integer_if_hex,
        'hls_gasPrice': to_integer_if_hex,
        'hls_getGasPrice': to_integer_if_hex,
        'hls_getBalance': to_integer_if_hex,
        'hls_getBlockTransactionCountByHash': to_integer_if_hex,
        'hls_getBlockTransactionCountByNumber': to_integer_if_hex,
        'hls_getCode': HexBytes,
        'hls_getStorageAt': HexBytes,
        'hls_getTransactionByBlockHashAndIndex': apply_formatter_if(
            is_not_null,
            transaction_formatter,
        ),
        'hls_getTransactionByBlockNumberAndIndex': apply_formatter_if(
            is_not_null,
            transaction_formatter,
        ),
        'hls_getTransactionReceipt': apply_formatter_if(
            is_not_null,
            receipt_formatter,
        ),
        'hls_getTransactionCount': to_integer_if_hex,
        'hls_protocolVersion': compose(
            apply_formatter_if(is_integer, str),
            to_integer_if_hex,
        ),
        'hls_getTransactionByHash': apply_formatter_if(is_not_null, transaction_formatter),
        'hls_getReceivableTransactions': apply_formatter_to_array(transaction_formatter),
        'hls_filterAddressesWithReceivableTransactions': apply_formatter_to_array(HexBytes),
        'hls_getReceiveTransactionOfSendTransaction': apply_formatter_if(is_not_null, transaction_formatter),
        'hls_getHistoricalGasPrice': apply_formatter_to_array(min_gas_price_formatter),
        'hls_getApproximateHistoricalNetworkTPCCapability': apply_formatter_to_array(min_gas_price_formatter),
        'hls_getApproximateHistoricalTPC': apply_formatter_to_array(min_gas_price_formatter),
        'hls_getBlockNumber':to_integer_if_hex,
        'hls_getBlockCreationParams': block_creation_parameters_formatter,
        'hls_getBlockByHash': apply_formatter_if(is_not_null, block_formatter),
        'hls_getBlockByNumber': apply_formatter_if(is_not_null, block_formatter),
        'hls_getConnectedNodes': apply_formatter_to_array(get_connected_nodes_formatter),
        'hls_call':HexBytes,
        # Net
        'net_peerCount': to_integer_if_hex,
    },
)
