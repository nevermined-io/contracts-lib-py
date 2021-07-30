from contracts_lib_py.contract_base import ContractBase


class GenericContract(ContractBase):
    """Class for instantiating any contract.

    Contract name is set at time of loading the contract.

    """


class GenericContractExternal(ContractBase):
    def __init__(self, address, abi, name, version='external'):
        from contracts_lib_py.contract_handler import ContractHandler

        self.name = name,
        self.CONTRACT_NAME = name
        self.version = version
        self.contract = ContractHandler.get_by_address(address, abi, name)