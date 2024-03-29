from collections import namedtuple

from contracts_lib_py import ContractBase

ConditionValues = namedtuple(
    'ConditionValues',
    ('type_ref', 'state', 'time_lock', 'time_out', 'block_number')
)


class ConditionStoreManager(ContractBase):
    """Class representing the ConditionStoreManager contract."""
    CONTRACT_NAME = 'ConditionStoreManager'

    def get_condition(self, condition_id):
        """Retrieve the condition for a condition_id.

        :param condition_id: id of the condition, str
        :return:
        """
        condition = self.contract.caller.getCondition(condition_id)
        if condition and len(condition) == 5:
            return ConditionValues(*condition)

        return None

    def get_condition_state(self, condition_id):
        """Retrieve the condition state.

        :param condition_id: id of the condition, str
        :return: State of the condition
        """
        return self.contract.caller.getConditionState(condition_id)

    def get_num_condition(self):
        """
        Return the size of the Conditions list.

        :return: the length of the conditions list, int
        """
        return self.contract.caller.getConditionListSize()
