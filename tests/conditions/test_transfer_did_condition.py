"""Test NFTHolderCondition contract."""
from contracts_lib_py.conditions.transfer_did import TransferDIDOwnershipCondition


def test_transfer_did_condition_contract():
    transfer_did_condition = TransferDIDOwnershipCondition('TransferDIDOwnershipCondition')
    assert transfer_did_condition
    assert isinstance(transfer_did_condition, TransferDIDOwnershipCondition), \
        f'{transfer_did_condition} is not instance of TransferDIDOwnershipCondition'
