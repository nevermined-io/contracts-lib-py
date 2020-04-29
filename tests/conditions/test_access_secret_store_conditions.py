"""Test AccessConditions contract."""
import uuid

from contracts_lib_py.conditions.access import AccessSecretStoreCondition
from tests.resources.helper_functions import get_consumer_account


def test_access_secret_store_condition_contract():
    access_secret_store_condition = AccessSecretStoreCondition('AccessSecretStoreCondition')
    assert access_secret_store_condition
    assert isinstance(access_secret_store_condition, AccessSecretStoreCondition), \
        f'{access_secret_store_condition} is not instance of AccessSecretStoreCondition'


def test_check_permissions_not_registered_did():
    access_secret_store_condition = AccessSecretStoreCondition('AccessSecretStoreCondition')
    consumer_account = get_consumer_account()
    did_id = uuid.uuid4().hex + uuid.uuid4().hex
    assert not access_secret_store_condition.check_permissions(did_id, consumer_account.address)

# TODO Create test for check permission after access granted.
