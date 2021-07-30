import json
import logging
import os

from web3 import Web3

from contracts_lib_py import Keeper
from contracts_lib_py.web3_provider import Web3Provider

logger = logging.getLogger(__name__)


class ContractHandler(object):
    """
    Manages loading contracts and also keeps a cache of loaded contracts.

    Retrieval of deployed keeper contracts must use this `ContractHandler`.
    Example:
        contract = ContractHandler.get('ServiceExecutionAgreement')
    """
    _contracts = dict()
    artifacts_path = None

    @staticmethod
    def get(name):
        """
        Return the Contract instance for a given name.

        :param name: Contract name, str
        :return: Contract instance
        """
        return (ContractHandler._contracts.get(name) or ContractHandler._load(name))[0]

    @staticmethod
    def get_by_address(address, abi, name):
        """
        Return the Contract instance for a given name.

        :param name: Contract name, str
        :return: Contract instance
        """
        return (ContractHandler._contracts.get(name) or ContractHandler._load_from_address(address, abi, name))[0]

    @staticmethod
    def get_contract_version(name):
        """
        Return the version of the contract in use.

        :param name: name of the contract
        :return: str version
        """
        return ContractHandler._contracts.get(name)[1]

    @staticmethod
    def set(name, contract):
        """
        Set a Contract instance for a contract name.

        :param name: Contract name, str
        :param contract: Contract instance
        """
        ContractHandler._contracts[name] = contract

    @staticmethod
    def has(name):
        """
        Check if a contract is the ContractHandler contracts.

        :param name: Contract name, str
        :return: True if the contract is there, bool
        """
        return name in ContractHandler._contracts

    @staticmethod
    def _load(contract_name):
        """Retrieve the contract instance for `contract_name` that represent the smart
        contract in the keeper network.

        :param contract_name: str name of the solidity keeper contract without the network name.
        :return: web3.eth.Contract instance
        """
        assert ContractHandler.artifacts_path is not None, 'artifacts_path should be already set.'
        contract_definition = ContractHandler.get_contract_dict_by_name(
            contract_name, ContractHandler.artifacts_path)
        address = Web3.toChecksumAddress(contract_definition['address'])
        abi = contract_definition['abi']
        contract = Web3Provider.get_web3().eth.contract(address=address, abi=abi)
        ContractHandler._contracts[contract_name] = (contract, contract_definition['version'])
        return ContractHandler._contracts[contract_name]

    @staticmethod
    def _load_from_address(address, abi, contract_name):
        """Retrieve the contract instance for `contract_name` that represent the smart
        contract in the keeper network.

        :param contract_name: str name of the solidity keeper contract without the network name.
        :return: web3.eth.Contract instance
        """
        address = Web3.toChecksumAddress(address)
        contract = Web3Provider.get_web3().eth.contract(address=address, abi=abi)
        ContractHandler._contracts[contract_name] = (contract, 'external')
        return ContractHandler._contracts[contract_name]

    @staticmethod
    def _get_contract_file_path(_base_path, _contract_name, _network_name, artifacts_path):
        contract_file_name = '{}.{}.json'.format(_contract_name, _network_name)
        for name in os.listdir(_base_path):
            if name.lower() == contract_file_name.lower():
                contract_file_name = name
                return os.path.join(artifacts_path, contract_file_name)
        return None

    @staticmethod
    def get_contract_dict_by_name(contract_name, artifacts_path):
        """
        Retrieve the Contract instance for a given contract name.

        :param contract_name: str
        :param artifacts_path: str the path to keeper contracts artifacts (`abi` .json files)
        :return: the smart contract's definition from the json abi file, dict
        """

        network_name = Keeper.get_network_name(Keeper.get_network_id()).lower()

        # file_name = '{}.{}.json'.format(contract_name, network_name)
        # path = os.path.join(keeper.artifacts_path, file_name)
        path = ContractHandler._get_contract_file_path(
            artifacts_path, contract_name, network_name, artifacts_path)
        if not (path and os.path.exists(path)):
            path = ContractHandler._get_contract_file_path(
                artifacts_path, contract_name, network_name.lower(), artifacts_path)

        if not (path and os.path.exists(path)):
            path = ContractHandler._get_contract_file_path(
                artifacts_path, contract_name, Keeper.DEFAULT_NETWORK_NAME, artifacts_path)

        if not (path and os.path.exists(path)):
            raise FileNotFoundError(
                f'Keeper contract {contract_name} file '
                f'not found in {artifacts_path} '
                f'using network name {network_name}'
            )

        with open(path) as f:
            contract_dict = json.loads(f.read())
            return contract_dict
