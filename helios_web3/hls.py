from helios_web3.account import (
    Account,
)
from eth_utils import (
    apply_to_return_value,
    is_checksum_address,
    is_string,
)

from web3.contract import (
    Contract,
)
from web3.iban import (
    Iban,
)
from web3.module import (
    Module,
)

from web3._utils.blocks import (
    select_method_for_block_identifier,
)
from web3._utils.empty import (
    empty,
)
from web3._utils.encoding import (
    to_hex,
)
from web3._utils.filters import (
    BlockFilter,
    LogFilter,
    TransactionFilter,
)
from eth_utils.toolz import (
    assoc,
    merge,
)
from web3._utils.transactions import (
    assert_valid_transaction_params,
    extract_valid_transaction_params,
    get_buffered_gas_estimate,
    get_required_transaction,
    replace_transaction,
    wait_for_transaction_receipt,
)

class Hls(Module):
    account = Account()
    defaultAccount = empty
    defaultBlock = "latest"
    defaultContractFactory = Contract
    iban = Iban
    gasPriceStrategy = None

    def call(self, transaction, block_identifier=None):
        if block_identifier is None:
            block_identifier = self.defaultBlock
        
        return self.web3.manager.request_blocking(
            "hls_call",
            [transaction, block_identifier],
        )
    
    def namereg(self):
        raise NotImplementedError()

    def icapNamereg(self):
        raise NotImplementedError()

    @property
    def ping(self):
        return self.web3.manager.request_blocking("hls_ping", [])

    @property
    def chainId(self):
        return self.web3.manager.request_blocking("hls_chainId", [])

    @property
    def protocolVersion(self):
        return self.web3.manager.request_blocking("hls_protocolVersion", [])

    @property
    def syncing(self):
        return self.web3.manager.request_blocking("hls_syncing", [])

    @property
    def coinbase(self):
        return self.web3.manager.request_blocking("hls_coinbase", [])

    @property
    def mining(self):
        return self.web3.manager.request_blocking("hls_mining", [])

    @property
    def hashrate(self):
        return self.web3.manager.request_blocking("hls_hashrate", [])

    @property
    def gasPrice(self):
        return self.web3.manager.request_blocking("hls_gasPrice", [])

    def getGasPrice(self):
        return self.web3.manager.request_blocking("hls_getGasPrice", [])

    @property
    def accounts(self):
        return self.web3.manager.request_blocking("hls_accounts", [])

    def blockNumber(self, chain_address):
        return self.web3.manager.request_blocking("hls_blockNumber", [chain_address])

    def getBalance(self, account, block_identifier=None):
        if block_identifier is None:
            block_identifier = self.defaultBlock
        return self.web3.manager.request_blocking(
            "hls_getBalance",
            [account, block_identifier],
        )

    def getStorageAt(self, account, position, block_identifier=None):
        if block_identifier is None:
            block_identifier = self.defaultBlock
        return self.web3.manager.request_blocking(
            "hls_getStorageAt",
            [account, position, block_identifier]
        )

    def getCode(self, account, block_identifier=None):
        if block_identifier is None:
            block_identifier = self.defaultBlock
        return self.web3.manager.request_blocking(
            "hls_getCode",
            [account, block_identifier],
        )

    def getBlock(self, block_identifier, full_transactions=False, chain_address = None):
        """
        `hls_getBlockByHash`
        `hls_getBlockByNumber`
        """
        method = select_method_for_block_identifier(
            block_identifier,
            if_predefined='hls_getBlockByNumber',
            if_hash='hls_getBlockByHash',
            if_number='hls_getBlockByNumber',
        )

        if method == 'hls_getBlockByHash':
            return self.web3.manager.request_blocking(
                method,
                [block_identifier, full_transactions],
            )
        else:
            if chain_address is None:
                raise TypeError("To get the block by block number, you must provide a chain address")

            return self.web3.manager.request_blocking(
                method,
                [block_identifier, chain_address, full_transactions],
            )


    def getBlockTransactionCount(self, block_identifier, chain_address = None):
        """
        `hls_getBlockTransactionCountByHash`
        `hls_getBlockTransactionCountByNumber`
        """
        method = select_method_for_block_identifier(
            block_identifier,
            if_predefined='hls_getBlockTransactionCountByNumber',
            if_hash='hls_getBlockTransactionCountByHash',
            if_number='hls_getBlockTransactionCountByNumber',
        )
        if method == 'hls_getBlockTransactionCountByNumber':
            if chain_address is None:
                raise TypeError("To get the block transaction count by block number, you must provide a chain address")
            return self.web3.manager.request_blocking(
                method,
                [block_identifier, chain_address],
            )
        else:
            return self.web3.manager.request_blocking(
                method,
                [block_identifier],
            )

    def getUncleCount(self, block_identifier):
        """
        `hls_getUncleCountByBlockHash`
        `hls_getUncleCountByBlockNumber`
        """
        method = select_method_for_block_identifier(
            block_identifier,
            if_predefined='hls_getUncleCountByBlockNumber',
            if_hash='hls_getUncleCountByBlockHash',
            if_number='hls_getUncleCountByBlockNumber',
        )
        return self.web3.manager.request_blocking(
            method,
            [block_identifier],
        )

    def getTransaction(self, transaction_hash):
        return self.web3.manager.request_blocking(
            "hls_getTransactionByHash",
            [transaction_hash],
        )

    def getTransactionFromBlock(self, block_identifier, transaction_index, chain_address = None):
        """
        `hls_getTransactionByBlockHashAndIndex`
        `hls_getTransactionByBlockNumberAndIndex`
        """
        method = select_method_for_block_identifier(
            block_identifier,
            if_predefined='hls_getTransactionByBlockNumberAndIndex',
            if_hash='hls_getTransactionByBlockHashAndIndex',
            if_number='hls_getTransactionByBlockNumberAndIndex',
        )
        if method == 'hls_getTransactionByBlockNumberAndIndex':
            if chain_address is None:
                raise TypeError("To get the block transaction count by block number, you must provide a chain address")
            return self.web3.manager.request_blocking(
                method,
                [block_identifier, transaction_index, chain_address],
            )
        else:
            return self.web3.manager.request_blocking(
                method,
                [block_identifier, transaction_index],
            )

    def waitForTransactionReceipt(self, transaction_hash, timeout=120):
        return wait_for_transaction_receipt(self.web3, transaction_hash, timeout)

    def getTransactionReceipt(self, transaction_hash):
        return self.web3.manager.request_blocking(
            "hls_getTransactionReceipt",
            [transaction_hash],
        )
    
    def getReceiveTransactionOfSendTransaction(self, transaction_hash):
        return self.web3.manager.request_blocking(
            "hls_getReceiveTransactionOfSendTransaction",
            [transaction_hash],
        )

    def getReceivableTransactions(self, chain_address):
        return self.web3.manager.request_blocking(
            "hls_getReceivableTransactions",
            [chain_address],
        )

    def filterAddressesWithReceivableTransactions(self, chain_addresses, after_timestamp = 0):
        return self.web3.manager.request_blocking(
            "hls_filterAddressesWithReceivableTransactions",
            [chain_addresses, after_timestamp],
        )


    def getTransactionCount(self, account, block_identifier=None):
        if block_identifier is None:
            block_identifier = self.defaultBlock
        return self.web3.manager.request_blocking(
            "hls_getTransactionCount",
            [
                account,
                block_identifier,
            ],
        )

    def replaceTransaction(self, transaction_hash, new_transaction):
        current_transaction = get_required_transaction(self.web3, transaction_hash)
        return replace_transaction(self.web3, current_transaction, new_transaction)

    def modifyTransaction(self, transaction_hash, **transaction_params):
        assert_valid_transaction_params(transaction_params)
        current_transaction = get_required_transaction(self.web3, transaction_hash)
        current_transaction_params = extract_valid_transaction_params(current_transaction)
        new_transaction = merge(current_transaction_params, transaction_params)
        return replace_transaction(self.web3, current_transaction, new_transaction)

    def sendTransaction(self, transaction):
        # TODO: move to middleware
        if 'from' not in transaction and is_checksum_address(self.defaultAccount):
            transaction = assoc(transaction, 'from', self.defaultAccount)

        # TODO: move gas estimation in middleware
        if 'gas' not in transaction:
            transaction = assoc(
                transaction,
                'gas',
                get_buffered_gas_estimate(self.web3, transaction),
            )

        return self.web3.manager.request_blocking(
            "hls_sendTransaction",
            [transaction],
        )

    def sendRawBlock(self, raw_block):
        return self.web3.manager.request_blocking(
            "hls_sendRawBlock",
            [raw_block],
        )

    def getBlockCreationParams(self, chain_address):
        return self.web3.manager.request_blocking(
            "hls_getBlockCreationParams",
            [chain_address],
        )

    def sign(self, account, data=None, hexstr=None, text=None):
        message_hex = to_hex(data, hexstr=hexstr, text=text)
        return self.web3.manager.request_blocking(
            "hls_sign", [account, message_hex],
        )


    def estimateGas(self, transaction):
        # TODO: move to middleware
        if 'from' not in transaction and is_checksum_address(self.defaultAccount):
            transaction = assoc(transaction, 'from', self.defaultAccount)

        return self.web3.manager.request_blocking(
            "hls_estimateGas",
            [transaction],
        )

    def filter(self, filter_params=None, filter_id=None):
        if filter_id and filter_params:
            raise TypeError(
                "Ambiguous invocation: provide either a `filter_params` or a `filter_id` argument. "
                "Both were supplied."
            )
        if is_string(filter_params):
            if filter_params == "latest":
                filter_id = self.web3.manager.request_blocking(
                    "hls_newBlockFilter", [],
                )
                return BlockFilter(self.web3, filter_id)
            elif filter_params == "pending":
                filter_id = self.web3.manager.request_blocking(
                    "hls_newPendingTransactionFilter", [],
                )
                return TransactionFilter(self.web3, filter_id)
            else:
                raise ValueError(
                    "The filter API only accepts the values of `pending` or "
                    "`latest` for string based filters"
                )
        elif isinstance(filter_params, dict):
            _filter_id = self.web3.manager.request_blocking(
                "hls_newFilter",
                [filter_params],
            )
            return LogFilter(self.web3, _filter_id)
        elif filter_id and not filter_params:
            return LogFilter(self.web3, filter_id)
        else:
            raise TypeError("Must provide either filter_params as a string or "
                            "a valid filter object, or a filter_id as a string "
                            "or hex.")

    def getFilterChanges(self, filter_id):
        return self.web3.manager.request_blocking(
            "hls_getFilterChanges", [filter_id],
        )

    def getFilterLogs(self, filter_id):
        return self.web3.manager.request_blocking(
            "hls_getFilterLogs", [filter_id],
        )

    def getLogs(self, filter_params):
        return self.web3.manager.request_blocking(
            "hls_getLogs", [filter_params],
        )

    def uninstallFilter(self, filter_id):
        return self.web3.manager.request_blocking(
            "hls_uninstallFilter", [filter_id],
        )

    def contract(self,
                 address=None,
                 **kwargs):
        ContractFactoryClass = kwargs.pop('ContractFactoryClass', self.defaultContractFactory)

        ContractFactory = ContractFactoryClass.factory(self.web3, **kwargs)

        if address:
            return ContractFactory(address)
        else:
            return ContractFactory

    def setContractFactory(self, contractFactory):
        self.defaultContractFactory = contractFactory

    def getCompilers(self):
        return self.web3.manager.request_blocking("hls_getCompilers", [])

    def getWork(self):
        return self.web3.manager.request_blocking("hls_getWork", [])

    def generateGasPrice(self, transaction_params=None):
        if self.gasPriceStrategy:
            return self.gasPriceStrategy(self.web3, transaction_params)

    def setGasPriceStrategy(self, gas_price_strategy):
        self.gasPriceStrategy = gas_price_strategy

    def devAddValidNewBlock(self, version=1):
        return self.web3.manager.request_blocking("hls_devAddValidNewBlock", [version])

    def devAddInvalidNewBlock(self, version=1):
        return self.web3.manager.request_blocking("hls_devAddInvalidNewBlock", [version])

    def test(self):
        return self.web3.manager.request_blocking("hls_test", [])

    def devDeploySmartContract(self):
        return self.web3.manager.request_blocking("hls_devDeploySmartContract", [])

    #
    # Dev tools
    #
    def getBlockchainDBDetails(self):
        return self.web3.manager.request_blocking("hls_getBlockchainDBDetails", [])

    def getCurrentStakeFromBootnodeList(self):
        return self.web3.manager.request_blocking("hls_getCurrentStakeFromBootnodeList", [])

    def getAccountBalances(self):
        return self.web3.manager.request_blocking("hls_getAccountBalances", [])

    def getChronologicalBlockWindowTimestampHashes(self, timestamp):
        return self.web3.manager.request_blocking("hls_getChronologicalBlockWindowTimestampHashes", [timestamp])

    def getHistoricalRootHashes(self):
        return self.web3.manager.request_blocking("hls_getHistoricalRootHashes", [])

    def getCurrentSyncingParameters(self):
        return self.web3.manager.request_blocking("hls_getCurrentSyncingParameters", [])

    def getBlockchainDatabase(self):
        return self.web3.manager.request_blocking("hls_getBlockchainDatabase", [])


    #
    # Gets
    #
    def getBlockByHash(self, block_hash, include_transactions=False):
        return self.web3.manager.request_blocking("hls_getBlockByHash", [block_hash, include_transactions])

    def getBlockByNumber(self, block_number, chain_address, include_transactions=False):
        return self.web3.manager.request_blocking("hls_getBlockByNumber",
                                                  [block_number, chain_address, include_transactions])

    def getHistoricalGasPrice(self):
        return self.web3.manager.request_blocking("hls_getHistoricalGasPrice",[])

    def getApproximateHistoricalNetworkTPCCapability(self):
        return self.web3.manager.request_blocking("hls_getApproximateHistoricalNetworkTPCCapability",[])

    def getApproximateHistoricalTPC(self):
        return self.web3.manager.request_blocking("hls_getApproximateHistoricalTPC",[])

    def getConnectedNodes(self):
        return self.web3.manager.request_blocking("hls_getConnectedNodes", [])

    #
    # Blocks
    #


    def getBlockNumber(self,account, block_identifier=None):
        if block_identifier is None:
            block_identifier = self.defaultBlock
        return self.web3.manager.request_blocking(
            "hls_getBlockNumber",
            [
                account,
                block_identifier,
            ],
        )

    def getNewestBlocks(self, num_to_return = '0xA', start_idx = '0x0', after_hash = '0x', chain_address = '0x', include_transactions: bool = False):

        return self.web3.manager.request_blocking(
            "hls_getNewestBlocks",
            [
                num_to_return,
                start_idx,
                after_hash,
                chain_address,
                include_transactions,
            ],
        )

