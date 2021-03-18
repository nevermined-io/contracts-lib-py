"""Test AccessConditions contract."""
import uuid

from contracts_lib_py.conditions.access import AccessCondition
from tests.resources.helper_functions import get_consumer_account


def test_access_condition_contract():
    access_secret_store_condition = AccessCondition('AccessCondition')
    assert access_secret_store_condition
    assert isinstance(access_secret_store_condition, AccessCondition), \
        f'{access_secret_store_condition} is not instance of AccessCondition'


def test_check_permissions_not_registered_did():
    access_secret_store_condition = AccessCondition('AccessCondition')
    consumer_account = get_consumer_account()
    did_id = uuid.uuid4().hex + uuid.uuid4().hex
    assert not access_secret_store_condition.check_permissions(did_id, consumer_account.address)

# TODO Create test for check permission after access granted.
