"""Test Dispenser contract."""

#  Copyright 2018 Ocean Protocol Foundation
#  SPDX-License-Identifier: Apache-2.0

import pytest

from contracts_lib_py.dispenser import Dispenser
from tests.resources.helper_functions import get_consumer_account
from tests.resources.tiers import e2e_test


@pytest.fixture()
def dispenser():
    return Dispenser.get_instance()


@e2e_test
def test_dispenser_contract(dispenser):
    assert dispenser
    assert isinstance(dispenser, Dispenser), f'{dispenser} is not instance of Market'


@e2e_test
def test_request_tokens(dispenser):
    account = get_consumer_account()
    assert dispenser.request_tokens(100, account), f'{account.address} do not get 100 tokens.'
