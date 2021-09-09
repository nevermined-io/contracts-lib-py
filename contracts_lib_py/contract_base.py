"""
    Keeper Contract Base

    All keeper contract inherit from this base class
"""
import logging

from web3 import Web3
from web3._utils.threads import Timeout

from contracts_lib_py.web3.contract import CustomContractFunction
from contracts_lib_py.web3_provider import Web3Provider

logger = logging.getLogger('keeper')


class ContractBase(object):
    """Base class for all contract objects."""
    CONTRACT_NAME = None
    ZERO_ADDRESS = '0x0000000000000000000000000000000000000000'

    def __init__(self, contract_name, dependencies=None):

        assert contract_name, 'param contract_name is required and must ' \
                              'match a valid keeper contract.'
        self.name = contract_name

        if not dependencies or 'ContractHandler' not in dependencies:
            dependencies = dict()
            from contracts_lib_py.contract_handler import ContractHandler
            dependencies['ContractHandler'] = ContractHandler

        self.contract = dependencies['ContractHandler'].get(contract_name)
        self.version = dependencies['ContractHandler'].get_contract_version(contract_name)

    @classmethod
    def get_instance(cls, dependencies=None):
        """
        Return an instance for a contract name.

        :param dependencies:
        :return: Contract base instance
        """
        assert cls is not ContractBase, 'ContractBase is not meant to be used directly.'
        assert cls.CONTRACT_NAME, 'CONTRACT_NAME must be set to a valid keeper contract name.'
        return cls(cls.CONTRACT_NAME, dependencies)

    @property
    def _contract(self):
        return self.contract

    @property
    def address(self):
        """Return the ethereum address of the solidity contract deployed
        in current keeper network.
        """
        return self._contract.address

    @property
    def events(self):
        """Expose the underlying contract's events.

        :return:
        """
        return self.contract.events

    @staticmethod
    def to_checksum_address(address):
        """
        Validate the address provided.

        :param address: Address, hex str
        :return: address, hex str
        """
        return Web3.toChecksumAddress(address)

    @staticmethod
    def to_checksum_addresses(addresses):
        """
        Calculate the checksum of an addresses array

        :param address: Address, hex str[]
        :return: address, hex str[]
        """

        hash = []
        for address in addresses:
            hash.append(Web3.toChecksumAddress(address))
        return hash

    @staticmethod
    def validate_token_address(token_address):
        if token_address is None or not Web3.isAddress(token_address):
            return ContractBase.ZERO_ADDRESS
        return token_address

    @staticmethod
    def get_tx_receipt(tx_hash):
        """
        Get the receipt of a tx.

        :param tx_hash: hash of the transaction
        :return: Tx receipt
        """
        try:
            tx_receipt = Web3Provider.get_web3().eth.waitForTransactionReceipt(tx_hash, timeout=20)
        except Timeout:
            logger.info('Waiting for transaction receipt timed out.')
            return
        except ValueError as e:
            logger.error(f'Waiting for transaction receipt failed: {e}')
            return

        return tx_receipt

    def is_tx_successful(self, tx_hash):
        receipt = self.get_tx_receipt(tx_hash)
        return bool(receipt and receipt.status == 1)

    def subscribe_to_event(self, event_name, timeout, event_filter, callback=None,
                           timeout_callback=None, args=None, wait=False,
                           from_block='latest', to_block='latest'):
        """
        Create a listener for the event choose.

        :param event_name: name of the event to subscribe, str
        :param timeout:
        :param event_filter:
        :param callback:
        :param timeout_callback:
        :param args:
        :param wait: if true block the listener until get the event, bool
        :param from_block: int or None
        :param to_block: int or None
        :return:
        """
        from contracts_lib_py.event_listener import EventListener
        return EventListener(
            self.CONTRACT_NAME,
            event_name,
            args,
            filters=event_filter,
            from_block=from_block,
            to_block=to_block
        ).listen_once(
            callback,
            timeout_callback=timeout_callback,
            timeout=timeout,
            blocking=wait
        )

    def send_transaction(self, fn_name, fn_args, transact=None):
        """Calls a smart contract function using either `personal_sendTransaction` (if
        passphrase is available) or `ether_sendTransaction`.

        :param fn_name: str the smart contract function name
        :param fn_args: tuple arguments to pass to function above
        :param transact: dict arguments for the transaction such as from, gas, etc.
        :return:
        """
        contract_fn = getattr(self.contract.functions, fn_name)(*fn_args)
        contract_function = CustomContractFunction(
            contract_fn
        )
        if transact is not None and 'chainId' not in transact:
            transact['chainId'] = int(Web3Provider.get_web3().net.version)
        return contract_function.transact(transact)

    def get_event_argument_names(self, event_name):
        event = getattr(self._contract.events, event_name, None)
        if event:
            return event().argument_names

    @property
    def function_names(self):
        return list(self._contract.function_names)

    def __str__(self):
        return f'{self.name} at {self.address}'
