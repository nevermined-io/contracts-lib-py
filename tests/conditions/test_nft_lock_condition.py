"""Test NFTLockCondition contract."""
from contracts_lib_py.conditions.nft_lock_condition import NFTLockCondition


def test_nft_lock_condition_contract():
    nft_lock_condition = NFTLockCondition('NFTLockCondition')
    assert nft_lock_condition
    assert isinstance(nft_lock_condition, NFTLockCondition), \
        f'{nft_lock_condition} is not instance of NFTLockCondition'