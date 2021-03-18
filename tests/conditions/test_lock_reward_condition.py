"""Test PaymentConditions contract."""
from contracts_lib_py.conditions.lock_reward import LockPaymentCondition


def test_lock_reward_condition_contract():
    lock_reward_condition = LockPaymentCondition('LockPaymentCondition')
    assert lock_reward_condition
    assert isinstance(lock_reward_condition, LockPaymentCondition), \
        f'{lock_reward_condition} is not instance of LockPaymentCondition'
