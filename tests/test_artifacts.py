import os

import pytest
from web3 import Web3
import nevermined_contracts

from contracts_lib_py.web3_provider import Web3Provider
from contracts_lib_py.web3.http_provider import CustomHTTPProvider
from contracts_lib_py.contract_handler import ContractHandler
from contracts_lib_py.keeper import Keeper

INFURA_TOKEN = os.environ.get("INFURA_TOKEN")

pytestmark = pytest.mark.integration


@pytest.mark.parametrize("keeper_url,network_id,network_name", [
    [f"https://mainnet.infura.io/v3/{INFURA_TOKEN}", [1], ["mainnet"]],
    [f"https://rinkeby.infura.io/v3/{INFURA_TOKEN}", [4], ["rinkeby"]],
    ("http://localhost:8545", [8996, 8997], ["spree", "polygon-localnet"]),
    (f"https://polygon-mumbai.infura.io/v3/{INFURA_TOKEN}", [80001], ["mumbai"]),
    ("https://alfajores-forno.celo-testnet.org", [44787], ["celo-alfajores"]),
    ("https://baklava-forno.celo-testnet.org", [62320], ["celo-baklava"])
    ],
    ids=[
        "mainnet",
        "rinkeby",
        "spree/polygon-localnet",
        "mumbai",
        "celo-alfajores",
        "celo-baklava"
    ]
)
def test_artifacts(keeper_url, network_id, network_name):
    Web3Provider._web3 = Web3(CustomHTTPProvider(keeper_url))
    ContractHandler.artifacts_path = nevermined_contracts.get_artifacts_path()
    keeper = Keeper()
    assert keeper.get_network_id() in network_id
    assert keeper.get_network_name(keeper.get_network_id()) in network_name
    assert keeper.did_registry is not None
