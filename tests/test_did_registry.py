"""Test DIDRegistry contract."""
import secrets
import uuid

import pytest
from eth_utils import add_0x_prefix
from web3 import Web3

from contracts_lib_py.didregistry import DIDRegistry
from tests.resources.helper_functions import get_consumer_account, get_publisher_account


def new_did():
    return uuid.uuid4().hex + uuid.uuid4().hex


def test_did_registry_contract():
    did_registry = DIDRegistry.get_instance()
    assert did_registry
    assert isinstance(did_registry, DIDRegistry)


def test_did_registry_get_block_number_updated():
    did_registry = DIDRegistry.get_instance()
    test_id = secrets.token_hex(32)
    assert did_registry.get_block_number_updated(test_id) == 0


def test_register():
    did_registry = DIDRegistry.get_instance()
    w3 = Web3
    _id = new_did()
    did_test = 'did:op:' + _id
    register_account = get_publisher_account()
    checksum_test = w3.sha3(text='checksum')
    value_test = 'http://localhost:5000'
    # register DID-> URL
    assert did_registry.register(
        _id, checksum_test, url=value_test, account=register_account
    ) is True

    with pytest.raises(Exception):
        did_registry.get_did_owner(did_test)

    assert did_registry.get_did_owner(
        add_0x_prefix(_id)
    ) == register_account.address


def test_register_with_invalid_params():
    did_registry = DIDRegistry.get_instance()
    w3 = Web3
    did_test = new_did()
    checksum_test = w3.sha3(text='checksum')
    value_test = 'http://localhost:5000'
    # No checksum provided
    with pytest.raises(ValueError):
        did_registry.register(did_test, '', url=value_test, account=None)
    # Invalid checksum  provided
    with pytest.raises(ValueError):
        did_registry.register(did_test, did_test, url=value_test, account=None)

    # No account provided
    with pytest.raises(ValueError):
        did_registry.register(did_test, checksum_test, url=value_test, account=None)


def test_providers():
    did_registry = DIDRegistry.get_instance()
    w3 = Web3
    did_test = new_did()
    asset_id = add_0x_prefix(did_test)
    register_account = get_publisher_account()
    consumer_account = get_consumer_account()
    checksum_test = w3.sha3(text='checksum')
    value_test = 'http://localhost:5000'
    test_address = w3.toChecksumAddress('068ed00cf0441e4829d9784fcbe7b9e26d4bd8d0')
    # register DID-> URL
    with pytest.raises(AssertionError):
        did_registry.register(
            did_test, checksum_test, url=value_test, account=register_account,
            providers=consumer_account.address
        )
    did_registry.register(
        did_test, checksum_test, url=value_test, account=register_account, providers=[test_address]
    )
    unknown_asset_id = add_0x_prefix(new_did())
    providers = did_registry.get_did_providers(unknown_asset_id)
    assert providers is None

    assert did_registry.is_did_provider(asset_id, register_account.address) is False

    providers = did_registry.get_did_providers(asset_id)
    assert len(providers) == 1 and providers[0] == test_address
    assert did_registry.is_did_provider(asset_id, test_address) is True

    removed = did_registry.remove_provider(asset_id, test_address, register_account)
    assert removed
    providers = did_registry.get_did_providers(asset_id)
    assert len(providers) == 0
    assert did_registry.is_did_provider(asset_id, test_address) is False

    did_registry.add_provider(asset_id, test_address, register_account)
    providers = did_registry.get_did_providers(asset_id)
    assert len(providers) == 1 and providers[0] == test_address
    assert did_registry.is_did_provider(asset_id, test_address) is True


def test_transfer_ownership():
    did_registry = DIDRegistry.get_instance()
    w3 = Web3
    did_test = new_did()
    asset_id = add_0x_prefix(did_test)
    register_account = get_publisher_account()
    consumer_account = get_consumer_account()
    checksum_test = w3.sha3(text='checksum')
    value_test = 'http://localhost:5000'
    test_address = w3.toChecksumAddress('068ed00cf0441e4829d9784fcbe7b9e26d4bd8d0')

    did_registry.register(did_test, checksum_test, url=value_test, account=register_account,
                          providers=[test_address])

    first_owner = did_registry.get_did_owner(did_test)
    assert first_owner == register_account.address

    did_registry.transfer_did_ownership(did_test, test_address, register_account)
    assert did_registry.get_did_owner(did_test) == test_address


def test_grant_permissions():
    did_registry = DIDRegistry.get_instance()
    w3 = Web3
    did_test = new_did()
    register_account = get_publisher_account()
    checksum_test = w3.sha3(text='checksum')
    value_test = 'http://localhost:5000'
    test_address = w3.toChecksumAddress('068ed00cf0441e4829d9784fcbe7b9e26d4bd8d0')

    did_registry.register(did_test, checksum_test, url=value_test, account=register_account,
                          providers=[test_address])

    assert not did_registry.get_permission(did_test, test_address)

    did_registry.grant_permission(did_test, test_address, register_account)

    assert did_registry.get_permission(did_test, test_address)

    did_registry.revoke_permission(did_test, test_address, register_account)

    assert not did_registry.get_permission(did_test, test_address)
