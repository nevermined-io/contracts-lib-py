"""Test Dispenser contract."""
import pytest

from contracts_lib_py.dispenser import Dispenser
from tests.resources.helper_functions import get_consumer_account


@pytest.fixture()
def dispenser():
    return Dispenser.get_instance()


def test_dispenser_contract(dispenser):
    assert dispenser
    assert isinstance(dispenser, Dispenser), f'{dispenser} is not instance of Market'


def test_request_tokens(dispenser):
    account = get_consumer_account()
    assert dispenser.request_tokens(100, account), f'{account.address} do not get 100 tokens.'
