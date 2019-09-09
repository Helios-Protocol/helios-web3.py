from web3._utils.rpc_abi import TRANSACTION_PARAMS_ABIS
FILTER_PARAMS_ABIS = {
    'to': 'address',
    'address': 'address[]',
}

RPC_ABIS = {
    # hls
    'hls_call': TRANSACTION_PARAMS_ABIS,
    'hls_estimateGas': TRANSACTION_PARAMS_ABIS,
    'hls_getBalance': ['address', None],
    'hls_getBlockByHash': ['bytes32', 'bool'],
    'hls_getBlockTransactionCountByHash': ['bytes32'],
    'hls_getCode': ['address', None],
    'hls_getLogs': FILTER_PARAMS_ABIS,
    'hls_getStorageAt': ['address', 'uint', None],
    'hls_getTransactionByBlockHashAndIndex': ['bytes32', 'uint'],
    'hls_getTransactionByHash': ['bytes32'],
    'hls_getTransactionCount': ['address', None],
    'hls_getTransactionReceipt': ['bytes32'],
    'hls_sendTransaction': TRANSACTION_PARAMS_ABIS,
    'hls_signTransaction': TRANSACTION_PARAMS_ABIS,
    'hls_sign': ['address', 'bytes'],
    'hls_signTypedData': ['address', None],
    # personal
    'personal_sendTransaction': TRANSACTION_PARAMS_ABIS,
    'personal_lockAccount': ['address'],
    'personal_unlockAccount': ['address', None, None],
    'personal_sign': [None, 'address', None],
    'personal_signTypedData': [None, 'address', None],
}