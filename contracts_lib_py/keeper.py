import logging
import os

from eth_utils import big_endian_to_int

from contracts_lib_py.agreements.agreement_manager import AgreementStoreManager
from contracts_lib_py.conditions.access import AccessSecretStoreCondition
from contracts_lib_py.conditions.compute_execution import ComputeExecutionCondition
from contracts_lib_py.conditions.condition_manager import ConditionStoreManager
from contracts_lib_py.conditions.escrow_reward import EscrowRewardCondition
from contracts_lib_py.conditions.hash_lock import HashLockCondition
from contracts_lib_py.conditions.lock_reward import LockRewardCondition
from contracts_lib_py.conditions.sign import SignCondition
from contracts_lib_py.conditions.threshold import ThresholdCondition
from contracts_lib_py.conditions.white_listing import WhitelistingCondition
from contracts_lib_py.didregistry import DIDRegistry
from contracts_lib_py.dispenser import Dispenser
from contracts_lib_py.generic_contract import GenericContract
from contracts_lib_py.templates.access_secret_store_template import EscrowAccessSecretStoreTemplate
from contracts_lib_py.templates.compute_execution_template import EscrowComputeExecutionTemplate
from contracts_lib_py.templates.template_manager import TemplateStoreManager
from contracts_lib_py.token import Token
from contracts_lib_py.utils import (add_ethereum_prefix_and_hash_msg, generate_multi_value_hash,
                                split_signature)
from contracts_lib_py.wallet import Wallet
from contracts_lib_py.web3.signature import SignatureFix
from contracts_lib_py.web3_provider import Web3Provider


class Keeper(object):
    """The Keeper class aggregates all contracts in the Nevermind Protocol node."""

    DEFAULT_NETWORK_NAME = 'development'
    _network_name_map = {
        1: 'Main',
        2: 'Morden',
        3: 'Ropsten',
        4: 'Rinkeby',
        42: 'Kovan',
        77: 'POA_Sokol',
        99: 'POA_Core',
        8995: 'nile',
        8996: 'spree',
        2199: 'duero',
        0xcea11: 'pacific'
    }

    def __init__(self, artifacts_path, contract_names=None):
        self.network_name = Keeper.get_network_name(Keeper.get_network_id())
        self.artifacts_path = artifacts_path
        self.accounts = Web3Provider.get_web3().eth.accounts
        self._contract_name_to_instance = {}
        if contract_names:
            for name in contract_names:
                contract = GenericContract(name)
                self._contract_name_to_instance = contract
                setattr(self, name, contract)

        self.dispenser = None
        if self.network_name != 'pacific':
            self.dispenser = Dispenser.get_instance()
        self.token = Token.get_instance()
        self.did_registry = DIDRegistry.get_instance()
        self.template_manager = TemplateStoreManager.get_instance()
        self.escrow_access_secretstore_template = EscrowAccessSecretStoreTemplate.get_instance()
        self.escrow_compute_execution_template = EscrowComputeExecutionTemplate.get_instance()
        self.agreement_manager = AgreementStoreManager.get_instance()
        self.condition_manager = ConditionStoreManager.get_instance()
        self.sign_condition = SignCondition.get_instance()
        self.lock_reward_condition = LockRewardCondition.get_instance()
        self.escrow_reward_condition = EscrowRewardCondition.get_instance()
        self.access_secret_store_condition = AccessSecretStoreCondition.get_instance()
        self.compute_execution_condition = ComputeExecutionCondition.get_instance()
        self.hash_lock_condition = HashLockCondition.get_instance()
        self.threshold_condition = ThresholdCondition.get_instance()
        self.white_listing_condition = WhitelistingCondition.get_instance()
        contracts = [
            self.token,
            self.did_registry,
            self.template_manager,
            self.escrow_access_secretstore_template,
            self.escrow_compute_execution_template,
            self.agreement_manager,
            self.condition_manager,
            self.sign_condition,
            self.lock_reward_condition,
            self.escrow_reward_condition,
            self.access_secret_store_condition,
            self.compute_execution_condition,
            self.hash_lock_condition,
            self.threshold_condition,
            self.white_listing_condition
        ]
        if self.dispenser:
            contracts.append(self.dispenser)
        self._contract_name_to_instance = {contract.name: contract
                                           for contract in contracts if contract}

    @staticmethod
    def get_instance(artifacts_path=None, contract_names=None):
        """Return the Keeper instance (singleton)."""
        return Keeper(artifacts_path, contract_names)

    @staticmethod
    def get_network_name(network_id):
        """
        Return the keeper network name based on the current ethereum network id.
        Return `development` for every network id that is not mapped.

        :param network_id: Network id, int
        :return: Network name, str
        """
        if os.environ.get('KEEPER_NETWORK_NAME'):
            logging.debug('keeper network name overridden by an environment variable: {}'.format(
                os.environ.get('KEEPER_NETWORK_NAME')))
            return os.environ.get('KEEPER_NETWORK_NAME')

        return Keeper._network_name_map.get(network_id, Keeper.DEFAULT_NETWORK_NAME)

    @staticmethod
    def get_network_id():
        """
        Return the ethereum network id calling the `web3.version.network` method.

        :return: Network id, int
        """
        return int(Web3Provider.get_web3().net.version)

    @staticmethod
    def sign_hash(msg_hash, account):
        """
        This method use `personal_sign`for signing a message. This will always prepend the
        `\x19Ethereum Signed Message:\n32` prefix before signing.

        :param msg_hash:
        :param account: Account
        :return: signature
        """
        wallet = Wallet(Web3Provider.get_web3(), account.key_file, account.password,
                        account.address)
        s = wallet.sign(msg_hash)
        return s.signature.hex()

    @staticmethod
    def ec_recover(message, signed_message):
        """
        This method does not prepend the message with the prefix `\x19Ethereum Signed Message:\n32`.
        The caller should add the prefix to the msg/hash before calling this if the signature was
        produced for an ethereum-prefixed message.

        :param message:
        :param signed_message:
        :return:
        """
        w3 = Web3Provider.get_web3()
        v, r, s = split_signature(w3, w3.toBytes(hexstr=signed_message))
        signature_object = SignatureFix(vrs=(v, big_endian_to_int(r), big_endian_to_int(s)))
        return w3.eth.account.recoverHash(message, signature=signature_object.to_hex_v_hacked())

    @staticmethod
    def personal_ec_recover(message, signed_message):
        prefixed_hash = add_ethereum_prefix_and_hash_msg(message)
        return Keeper.ec_recover(prefixed_hash, signed_message)

    @staticmethod
    def unlock_account(account):
        """
        Unlock the account.

        :param account: Account
        :return:
        """
        return Web3Provider.get_web3().personal.unlockAccount(account.address, account.password)

    @staticmethod
    def get_ether_balance(address):
        """
        Get balance of an ethereum address.

        :param address: address, bytes32
        :return: balance, int
        """
        return Web3Provider.get_web3().eth.getBalance(address, block_identifier='latest')

    @property
    def contract_name_to_instance(self):
        return self._contract_name_to_instance

    def get_contract(self, contract_name):
        contract = self.contract_name_to_instance.get(contract_name)
        if contract:
            return contract

        try:
            return GenericContract(contract_name)
        except Exception as e:
            logging.error(f'Cannot load contract {contract_name}: {e}')
            return None

    @staticmethod
    def generate_multi_value_hash(types, values):
        return generate_multi_value_hash(types, values)
