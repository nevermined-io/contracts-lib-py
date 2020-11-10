import os

import pytest
from web3 import HTTPProvider, Web3

from tests.resources.helper_functions import (
    get_consumer_account,
    get_publisher_account,
    setup_keeper,
    get_keeper_url
)


@pytest.fixture(autouse=True)
def setup_all():
   setup_keeper()


@pytest.fixture
def publisher_account():
    return get_publisher_account()


@pytest.fixture
def consumer_account():
    return get_consumer_account()


@pytest.fixture
def web3_instance():
    return Web3(HTTPProvider(get_keeper_url()))
