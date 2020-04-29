"""Test PaymentConditions contract."""
from contracts_lib_py.conditions.lock_reward import LockRewardCondition


def test_lock_reward_condition_contract():
    lock_reward_condition = LockRewardCondition('LockRewardCondition')
    assert lock_reward_condition
    assert isinstance(lock_reward_condition, LockRewardCondition), \
        f'{lock_reward_condition} is not instance of LockRewardCondition'
