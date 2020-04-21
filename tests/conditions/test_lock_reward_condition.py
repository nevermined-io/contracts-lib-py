"""Test PaymentConditions contract."""
#  Copyright 2018 Ocean Protocol Foundation
#  SPDX-License-Identifier: Apache-2.0

from contracts_lib_py.conditions.lock_reward import LockRewardCondition
from tests.resources.tiers import e2e_test


@e2e_test
def test_lock_reward_condition_contract():
    lock_reward_condition = LockRewardCondition('LockRewardCondition')
    assert lock_reward_condition
    assert isinstance(lock_reward_condition, LockRewardCondition), \
        f'{lock_reward_condition} is not instance of LockRewardCondition'
