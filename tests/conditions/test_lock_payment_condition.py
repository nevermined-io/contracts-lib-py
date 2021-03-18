"""Test PaymentConditions contract."""
from contracts_lib_py.conditions.lock_reward import LockPaymentCondition


def test_lock_payment_condition_contract():
    lock_payment_condition = LockPaymentCondition('LockPaymentCondition')
    assert lock_payment_condition
    assert isinstance(lock_payment_condition, LockPaymentCondition), \
        f'{lock_payment_condition} is not instance of LockPaymentCondition'
