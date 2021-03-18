"""Test Token Contract."""
import pytest
from web3 import Web3

from contracts_lib_py.conditions import LockPaymentCondition
from contracts_lib_py.token import Token
from contracts_lib_py.keeper import Keeper
from tests.resources.helper_functions import get_consumer_account, get_publisher_account, get_network_name

consumer_account = get_consumer_account()
publisher_account = get_publisher_account()


# skip NeverminedToken tests if not running on the spree network
pytestmark = pytest.mark.skipif(
    get_network_name() != "spree",
    reason="NeverminedToken tests should only run on the `spree` network"
)


def test_token_contract():
    token = Token.get_instance()
    assert token
    assert isinstance(token, Token)


def test_get_balance():
    token = Token.get_instance()
    assert isinstance(token.get_token_balance(consumer_account.address), int)


def test_get_balance_invalid_address():
    token = Token.get_instance()
    with pytest.raises(Exception):
        token.get_token_balance('not valid')


def test_token_approve():
    token = Token.get_instance()
    assert token.token_approve(consumer_account.address, 100, publisher_account)


def test_token_approve_invalid_address():
    token = Token.get_instance()
    with pytest.raises(Exception):
        token.token_approve('10923019', 100, publisher_account)


def test_token_approve_invalid_tokens():
    token = Token.get_instance()
    with pytest.raises(Exception):
        token.token_approve(consumer_account.address, -100, publisher_account)


def test_token_allowance():
    token = Token.get_instance()
    lock_reward_condition = LockPaymentCondition(LockPaymentCondition.CONTRACT_NAME)
    allowance = token.get_allowance(consumer_account.address, lock_reward_condition.address)
    if allowance > 0:
        token.decrease_allowance(lock_reward_condition.address, allowance, consumer_account)
        allowance = token.get_allowance(consumer_account.address, lock_reward_condition.address)
    assert allowance == 0

    assert token.token_approve(lock_reward_condition.address, 77, consumer_account) is True
    allowance = token.get_allowance(consumer_account.address, lock_reward_condition.address)
    assert allowance == 77

    assert token.token_approve(lock_reward_condition.address, 49, consumer_account) is True
    allowance = token.get_allowance(consumer_account.address, lock_reward_condition.address)
    assert allowance == 49

    token.decrease_allowance(lock_reward_condition.address, 5, consumer_account)
    allowance = token.get_allowance(consumer_account.address, lock_reward_condition.address)
    assert allowance == 44

    token.increase_allowance(lock_reward_condition.address, 10, consumer_account)
    allowance = token.get_allowance(consumer_account.address, lock_reward_condition.address)
    assert allowance == 54


def test_token_transfer():
    test_address = Web3.toChecksumAddress('068ed00cf0441e4829d9784fcbe7b9e26d4bd8d0')
    token = Token.get_instance()
    balance = token.get_token_balance(test_address)
    token.transfer(test_address, 3, consumer_account)
    new_balance = token.get_token_balance(test_address)
    assert new_balance == (balance + 3)
