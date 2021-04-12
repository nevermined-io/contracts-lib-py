"""Test DIDRegistry contract."""
import secrets
import uuid

import pytest
from eth_utils import add_0x_prefix
from web3 import Web3

from contracts_lib_py import Keeper
from contracts_lib_py.contract_handler import ContractHandler
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
    checksum_test = w3.keccak(text='checksum')
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
    checksum_test = w3.keccak(text='checksum')
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
    checksum_test = w3.keccak(text='checksum')
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
    assert len(providers) == 0

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
    checksum_test = w3.keccak(text='checksum')
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
    checksum_test = w3.keccak(text='checksum')
    value_test = 'http://localhost:5000'
    test_address = w3.toChecksumAddress('068ed00cf0441e4829d9784fcbe7b9e26d4bd8d0')

    did_registry.register(did_test, checksum_test, url=value_test, account=register_account,
                          providers=[test_address])

    assert not did_registry.get_permission(did_test, test_address)

    did_registry.grant_permission(did_test, test_address, register_account)

    assert did_registry.get_permission(did_test, test_address)

    did_registry.revoke_permission(did_test, test_address, register_account)

    assert not did_registry.get_permission(did_test, test_address)


def test_provenance_events():
    did_registry = DIDRegistry.get_instance()
    w3 = Web3
    did_test = new_did()
    register_account = get_publisher_account()
    checksum_test = w3.keccak(text='checksum')
    activity_id = new_did()
    provenance_id = new_did()
    url = 'http://localhost:5000'
    test_address = w3.toChecksumAddress('068ed00cf0441e4829d9784fcbe7b9e26d4bd8d0')

    assert did_registry.register(did_test, checksum_test, url=url, account=register_account,
                                 providers=[test_address], activity_id=activity_id) is True

    did_registry.used(provenance_id, did_test, test_address, activity_id, "",
                      account=register_account, attributes="used test")

    assert len(did_registry.get_did_provenance_events(Web3.toBytes(hexstr=did_test))) == 2


def test_provenance_from_registry():
    did_registry = DIDRegistry.get_instance()
    w3 = Web3
    did_test = new_did()
    register_account = get_publisher_account()
    checksum_test = w3.keccak(text='checksum')
    activity_id = new_did()
    provenance_id = new_did()
    url = 'http://localhost:5000'
    test_address = w3.toChecksumAddress('068ed00cf0441e4829d9784fcbe7b9e26d4bd8d0')

    assert did_registry.register(did_test, checksum_test, url=url, account=register_account,
                                 providers=[test_address], activity_id=activity_id) is True

    assert register_account.address == did_registry.get_provenance_owner(did_test)

    did_registry.used(provenance_id, did_test, test_address, activity_id, "",
                      account=register_account, attributes="used test")

    provenance_entry = did_registry.get_provenance_entry(provenance_id)
    assert ("0x" + activity_id, provenance_entry['activity_id'])
    assert ("0x" + did_test, provenance_entry['did'])
    assert (3, provenance_entry['method'])
    assert (register_account.address, provenance_entry['created_by'])


def test_delegate_provenance():
    did_registry = DIDRegistry.get_instance()
    w3 = Web3
    did_test = new_did()
    register_account = get_publisher_account()
    delegated_account = get_consumer_account()
    checksum_test = w3.keccak(text='checksum')
    activity_id = new_did()
    provenance_id = new_did()
    url = 'http://localhost:5000'
    test_address = w3.toChecksumAddress('068ed00cf0441e4829d9784fcbe7b9e26d4bd8d0')

    assert did_registry.register(did_test, checksum_test, url=url, account=register_account,
                                 providers=[test_address], activity_id=activity_id) is True

    assert did_registry.is_provenance_delegate(Web3.toBytes(hexstr=did_test),
                                               register_account.address) is False
    assert did_registry.is_provenance_delegate(Web3.toBytes(hexstr=did_test),
                                               delegated_account.address) is False
    assert did_registry.add_did_provenance_delegate(Web3.toBytes(hexstr=did_test),
                                                    delegated_account.address,
                                                    register_account) is True
    assert did_registry.is_provenance_delegate(Web3.toBytes(hexstr=did_test),
                                               delegated_account.address) is True
    assert did_registry.remove_did_provenance_delegate(Web3.toBytes(hexstr=did_test),
                                                       delegated_account.address,
                                                       register_account) is True
    assert did_registry.is_provenance_delegate(Web3.toBytes(hexstr=did_test),
                                               delegated_account.address) is False


def test_search_multiple_provenance_event_tests():
    did_registry = DIDRegistry.get_instance()
    w3 = Web3
    did_test = new_did()
    register_account = get_publisher_account()
    checksum_test = w3.keccak(text='checksum')
    activity_id = new_did()
    provenance_id = new_did()
    derived_did = new_did()
    url = 'http://localhost:5000'
    test_address = w3.toChecksumAddress('068ed00cf0441e4829d9784fcbe7b9e26d4bd8d0')

    assert did_registry.register(did_test, checksum_test, url=url, account=register_account,
                                 providers=[test_address], activity_id=activity_id) is True

    did_registry.used(provenance_id, did_test, register_account.address, activity_id, "",
                      account=register_account, attributes="used test")

    did_registry.was_derived_from(new_did(), derived_did, did_test, register_account.address,
                                  activity_id,
                                  account=register_account, attributes="was derived from")

    did_registry.was_associated_with(new_did(), did_test, register_account.address, activity_id,
                                     account=register_account, attributes="was associated with")

    did_registry.acted_on_behalf(new_did(), did_test, register_account.address,
                                 register_account.address, activity_id, '',
                                 account=register_account, attributes="acted on behalf")

    assert len(did_registry.get_provenance_method_events('WAS_GENERATED_BY',
                                                         Web3.toBytes(hexstr=did_test))) == 1
    assert len(
        did_registry.get_provenance_method_events('USED', Web3.toBytes(hexstr=did_test))) == 1
    assert len(did_registry.get_provenance_method_events('WAS_DERIVED_FROM',
                                                         Web3.toBytes(hexstr=derived_did))) == 1
    assert len(did_registry.get_provenance_method_events('WAS_ASSOCIATED_WITH',
                                                         Web3.toBytes(hexstr=did_test))) == 1

    assert len(did_registry.get_provenance_method_events('ACTED_ON_BEHALF',
                                                         Web3.toBytes(hexstr=did_test))) == 1


def test_royalties_are_valid():
    did_registry = DIDRegistry.get_instance()
    w3 = Web3
    did_test = new_did()
    register_account = get_publisher_account()
    checksum_test = w3.keccak(text='checksum')
    activity_id = new_did()
    new_owner_address = w3.toChecksumAddress('068ed00cf0441e4829d9784fcbe7b9e26d4bd8d0')
    someone_address = w3.toChecksumAddress('0x00a329c0648769A73afAc7F9381E08FB43dBEA72')
    url = 'http://localhost:5000'
    royalties = 20
    cap = 0

    assert did_registry.register_mintable_did(did_test, checksum_test, url, cap, royalties, account=register_account,
                                              providers=[someone_address], activity_id=activity_id) is True

    did_registry.transfer_did_ownership(did_test, new_owner_address, register_account)

    assert did_registry.are_royalties_valid(did_test, [80, 20], [someone_address, register_account.address]) is True
    assert did_registry.are_royalties_valid(did_test, [90], [someone_address]) is False
    assert did_registry.are_royalties_valid(did_test, [90, 10], [someone_address, register_account.address]) is False


def test_get_did():
    did_registry = DIDRegistry.get_instance()
    w3 = Web3
    did_test = new_did()
    register_account = get_publisher_account()
    checksum_test = w3.keccak(text='checksum')
    activity_id = new_did()
    someone_address = w3.toChecksumAddress('0x00a329c0648769A73afAc7F9381E08FB43dBEA72')
    url = 'http://localhost:5000'
    royalties = 20
    cap = 0

    assert did_registry.register_mintable_did(did_test, checksum_test, url, cap, royalties, account=register_account,
                                              providers=[someone_address], activity_id=activity_id) is True

    registered_did = did_registry.get_did_register(did_test)
    assert registered_did['owner'] == register_account.address
    assert registered_did['url'] == url
    assert registered_did['lastUpdatedBy'] == register_account.address
    assert registered_did['blockNumberUpdated'] > 0
    assert len(registered_did['providers']) == 1
    assert registered_did['nftSupply'] == 0
    assert registered_did['mintCap'] == cap
    assert registered_did['royalties'] == royalties


def test_nft():
    did_registry = DIDRegistry.get_instance()
    w3 = Web3
    did_test = new_did()
    register_account = get_publisher_account()
    someone_address = "0x00a329c0648769A73afAc7F9381E08FB43dBEA72"
    checksum_test = w3.keccak(text='checksum')
    activity_id = new_did()
    cap = 10
    royalties = 0
    url = 'http://localhost:5000'
    test_address = w3.toChecksumAddress('068ed00cf0441e4829d9784fcbe7b9e26d4bd8d0')

    assert did_registry.register_mintable_did(did_test, checksum_test, url, cap, royalties, account=register_account,
                                              providers=[test_address], activity_id=activity_id) is True

    balance = did_registry.balance(register_account.address, did_test)
    assert balance == 0
    balance_consumer = did_registry.balance(someone_address, did_test)
    assert balance_consumer == 0

    did_registry.mint(did_test, 10, account=register_account)
    assert balance + 10 == did_registry.balance(register_account.address, did_test)
    assert did_registry.transfer_nft(did_test, someone_address, 1, register_account)
    assert did_registry.balance(register_account.address, did_test) == 9
    assert did_registry.balance(someone_address, did_test) == balance_consumer + 1
    did_registry.burn(did_test, 9, account=register_account)
    assert balance == did_registry.balance(register_account.address, did_test)


def test_nft_approval():
    did_registry = DIDRegistry.get_instance()
    w3 = Web3
    keeper = Keeper(ContractHandler.artifacts_path)

    assert did_registry.is_nft_approved_for_all(w3.toChecksumAddress('068ed00cf0441e4829d9784fcbe7b9e26d4bd8d0'),
                                                keeper.transfer_nft_condition.address) is True

    assert did_registry.is_nft_approved_for_all(w3.toChecksumAddress('068ed00cf0441e4829d9784fcbe7b9e26d4bd8d0'),
                                                keeper.did_sales_template.address) is False



