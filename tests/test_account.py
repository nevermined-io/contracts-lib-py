"""Test the Account object."""
from contracts_lib_py.account import Account


def test_create_account():
    account = Account('0x213123123', 'pass')
    assert isinstance(account, Account)
    assert account.address == '0x213123123'
    assert account.password == 'pass'
