"""Test NFTHolderCondition contract."""
from web3 import Web3

from contracts_lib_py.conditions.transfer_nft import TransferNFTCondition


def test_transfer_nft_condition_contract():
    transfer_nft_condition = TransferNFTCondition('TransferNFTCondition')
    assert transfer_nft_condition
    assert isinstance(transfer_nft_condition, TransferNFTCondition), \
        f'{transfer_nft_condition} is not instance of TransferNFTCondition'


def test_transfer_nft_default_address():
    transfer_nft_condition = TransferNFTCondition('TransferNFTCondition')
    default_address = transfer_nft_condition.get_nft_default_address()
    print('Default NFT Contract address in Transfer Condition ' + default_address)
    assert Web3.isAddress(default_address)
