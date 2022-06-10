import os
import tarfile
from tempfile import TemporaryDirectory

import pytest
from web3 import Web3
import requests

from contracts_lib_py.web3_provider import Web3Provider
from contracts_lib_py.web3.http_provider import CustomHTTPProvider
from contracts_lib_py.contract_handler import ContractHandler
from contracts_lib_py.keeper import Keeper

INFURA_TOKEN = os.environ.get("INFURA_TOKEN")
ARTIFACTS_REPO = os.environ.get("ARTIFACTS_REPO", 'https://artifacts.nevermined.rocks/')

pytestmark = pytest.mark.integration


@pytest.mark.parametrize("keeper_url,network_id,network_name,version,tag", [
    # [f"https://mainnet.infura.io/v3/{INFURA_TOKEN}", [1], ["mainnet"], 'v1.3.8', 'common'],
    # [f"https://rinkeby.infura.io/v3/{INFURA_TOKEN}", [4], ["rinkeby"], 'v1.3.8', 'common'],
    (f"https://polygon-mumbai.infura.io/v3/{INFURA_TOKEN}", 80001, "mumbai", 'v1.3.8', 'common'),
    ("https://alfajores-forno.celo-testnet.org", 44787, "celo-alfajores", 'v1.3.8', 'common'),
    # (f"https://polygon-mainnet.infura.io/v3/{INFURA_TOKEN}", [137], ["matic"], 'v1.3.8', 'common'),
    # ("https://forno.celo.org", 42220, "celo", 'v1.3.8', 'common')
    ],
    ids=[
        # "mainnet",
        # "rinkeby",
        # "mumbai",
        "celo-alfajores",
        "matic",
        # "celo"
    ]
)
def test_artifacts(keeper_url, network_id, network_name, version, tag):
    with TemporaryDirectory() as tmp:
        artifacts_path = f'{tmp}/artifacts'
        package_name = f'contracts_{version}.tar.gz'
        package_path = f'{tmp}/{package_name}'
        artifacts_url = f'{ARTIFACTS_REPO}{network_id}/{tag}/{package_name}'

        r = requests.get(artifacts_url)

        with open(package_path, 'wb+') as f:
            f.write(r.content)
            f.flush()

        tar = tarfile.open(package_path)
        tar.extractall(artifacts_path)

        Web3Provider._web3 = Web3(CustomHTTPProvider(keeper_url))
        ContractHandler.artifacts_path = artifacts_path
        keeper = Keeper()
        assert keeper.get_network_id() == network_id
        assert keeper.get_network_name(keeper.get_network_id()) == network_name
        assert keeper.did_registry is not None
