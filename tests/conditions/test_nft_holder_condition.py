"""Test NFTHolderCondition contract."""
from contracts_lib_py.conditions.nft_holder import NFTHolderCondition


def test_lock_payment_condition_contract():
    nft_holder_condition = NFTHolderCondition('NFTHolderCondition')
    assert nft_holder_condition
    assert isinstance(nft_holder_condition, NFTHolderCondition), \
        f'{nft_holder_condition} is not instance of NFTHolderCondition'
