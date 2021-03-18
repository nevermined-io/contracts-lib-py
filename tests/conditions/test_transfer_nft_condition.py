"""Test NFTHolderCondition contract."""
from contracts_lib_py.conditions.transfer_nft import TransferNFTCondition


def test_transfer_did_condition_contract():
    transfer_nft_condition = TransferNFTCondition('TransferNFTCondition')
    assert transfer_nft_condition
    assert isinstance(transfer_nft_condition, TransferNFTCondition), \
        f'{transfer_nft_condition} is not instance of TransferNFTCondition'
