"""Test AccessConditions contract."""
import uuid

from contracts_lib_py.conditions.access import AccessCondition
from contracts_lib_py.conditions.nft_access import NFTAccessCondition
from tests.resources.helper_functions import get_consumer_account


def test_access_condition_contract():
    access_condition = AccessCondition('AccessCondition')
    assert access_condition
    assert isinstance(access_condition, AccessCondition), \
        f'{access_condition} is not instance of AccessCondition'


def test_nft_access_condition_contract():
    nft_access_condition = NFTAccessCondition('NFTAccessCondition')
    assert nft_access_condition
    assert isinstance(nft_access_condition, NFTAccessCondition), \
        f'{nft_access_condition} is not instance of NFTAccessCondition'


def test_check_permissions_not_registered_did():
    access_condition = AccessCondition('AccessCondition')
    consumer_account = get_consumer_account()
    did_id = uuid.uuid4().hex + uuid.uuid4().hex
    assert not access_condition.check_permissions(did_id, consumer_account.address)

# TODO Create test for check permission after access granted.
