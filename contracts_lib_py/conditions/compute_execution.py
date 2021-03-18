from contracts_lib_py.conditions.condition_base import ConditionBase


class ComputeExecutionCondition(ConditionBase):
    """Class representing the ComputeExecutionCondition contract."""
    CONTRACT_NAME = 'ComputeExecutionCondition'

    def fulfill(self, agreement_id, did, computer_consumer_address, account):
        """
        Fulfill the compute execution condition.

        :param agreement_id: id of the agreement, hex str
        :param did: the id of an asset on-chain, hex str
        :param computer_consumer_address: is the address of the consumer user, str
        :param account: Account instance
        :return: true if the condition was successfully fulfilled, bool
        """
        return self._fulfill(
            agreement_id,
            did,
            computer_consumer_address,
            transact={'from': account.address,
                      'passphrase': account.password,
                      'keyfile': account.key_file}
        )

    def hash_values(self, did, computer_consumer_address):
        """
        Hash the values of the compute execution condition.

        :param did: the id of an asset on-chain, hex str
        :param computer_consumer_address: is the address of the consumer user, str
        :return: hex str
        """
        return self._hash_values(did, computer_consumer_address)

    def was_compute_triggered(self, did, computer_consumer_address):
        """
        Checks whether the compute is triggered or not.

        :param did: the id of an asset on-chain, hex str
        :param computer_consumer_address: is the address of the consumer user, str
        :return: bool
        """
        return self.contract.caller.wasComputeTriggered(did, computer_consumer_address)
