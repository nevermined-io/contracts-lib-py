from contracts_lib_py.conditions.condition_base import ConditionBase


class ThresholdCondition(ConditionBase):
    """Class representing the ThresholdCondition contract."""
    CONTRACT_NAME = 'ThresholdCondition'

    def fulfill(self, agreement_id, input_conditions, threshold, from_account):
        """
        Fulfill the Threshold condition

        :param agreement_id: id of the agreement, hex str
        :param input_conditions: array of input conditions IDs
        :param threshold: the required number of fulfilled input conditions, int
        :param from_account: Account instance
        :return:
        """
        assert len(input_conditions) >= 2, 'The minimum number of conditions is 2.'
        assert threshold <= len(input_conditions), \
            'The required number of condition to be fulfilled(threshold) should ' \
            'be smaller than the number of conditions.'
        return self._fulfill(
            agreement_id,
            input_conditions,
            threshold,
            transact={'from': from_account.address,
                      'passphrase': from_account.password,
                      'keyfile': from_account.key_file}
        )

    def hash_values(self, input_conditions, threshold):
        """
        HashValues generates the hash of condition inputs with the following parameters

        :param input_conditions: array of input conditions IDs
        :param threshold: the required number of fulfilled input conditions, int
        :return: hex str
        """
        return self._hash_values(input_conditions, threshold)

    def can_fulfill(self, input_conditions, threshold):
        """
        Check if condition can be fulfilled

        :param input_conditions: array of input conditions IDs
        :param threshold: the required number of fulfilled input conditions, int
        :return:
        """
        return self.contract.caller.canFulfill(input_conditions, threshold)
