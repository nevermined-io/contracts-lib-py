import os
import pathlib

from web3 import Web3

from contracts_lib_py import Keeper
from contracts_lib_py.utils import get_account
from contracts_lib_py.web3_provider import Web3Provider
from contracts_lib_py.keeper import Keeper
from contracts_lib_py.contract_handler import ContractHandler
from contracts_lib_py.web3.http_provider import CustomHTTPProvider



PUBLISHER_INDEX = 1
CONSUMER_INDEX = 0


def get_keeper_url():
    if os.getenv('KEEPER_URL'):
        return os.getenv('KEEPER_URL')
    return 'http://localhost:8545'


def setup_keeper():
    Web3Provider._web3 = Web3(CustomHTTPProvider(get_keeper_url()))
    ContractHandler.artifacts_path = os.path.expanduser('~/.nevermined/nevermined-contracts/artifacts')
    Keeper.get_instance(artifacts_path=ContractHandler.artifacts_path)


def get_network_name():
    setup_keeper()
    return Keeper.get_network_name(Keeper.get_network_id())


def get_resource_path(dir_name, file_name):
    base = os.path.realpath(__file__).split(os.path.sep)[1:-1]
    if dir_name:
        return pathlib.Path(os.path.join(os.path.sep, *base, dir_name, file_name))
    else:
        return pathlib.Path(os.path.join(os.path.sep, *base, file_name))


def init_ocn_tokens(ocn, account, amount=100):
    ocn.accounts.request_tokens(account, amount)
    Keeper.get_instance().token.token_approve(
        Keeper.get_instance().dispenser.address,
        amount,
        account
    )


def get_publisher_account():
    return get_account(0)


def get_consumer_account():
    return get_account(0)
