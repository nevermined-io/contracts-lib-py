import os

import pytest
from web3 import Web3
import nevermined_contracts

from contracts_lib_py.web3_provider import Web3Provider
from contracts_lib_py.web3.http_provider import CustomHTTPProvider
from contracts_lib_py.contract_handler import ContractHandler
from contracts_lib_py.keeper import Keeper

INFURA_TOKEN = os.environ.get("INFURA_TOKEN")


@pytest.mark.parametrize("keeper_url,network_id,network_name", [
    [f"https://mainnet.infura.io/v3/{INFURA_TOKEN}", 1, "mainnet"],
    [f"https://rinkeby.infura.io/v3/{INFURA_TOKEN}", 4, "rinkeby"],
    ("http://localhost:8545", 8996, "spree"),
    ("https://rpc-mumbai.matic.today", 80001, "mumbai"),
    ("https://alfajores-forno.celo-testnet.org", 44787, "celo-alfajores"),
    ("https://baklava-forno.celo-testnet.org", 62320, "celo-baklava")
])
def test_artifacts(keeper_url, network_id, network_name):
    Web3Provider._web3 = Web3(CustomHTTPProvider(keeper_url))
    ContractHandler.artifacts_path = nevermined_contracts.get_artifacts_path()
    keeper = Keeper()
    assert keeper.get_network_id() == network_id
    assert keeper.get_network_name(keeper.get_network_id()) == network_name
    assert keeper.did_registry is not None
