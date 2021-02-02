from contracts_lib_py.conditions.condition_base import ConditionBase

from contracts_lib_py import utils

class EscrowRewardCondition(ConditionBase):
    """Class representing the EscrowReward contract."""
    CONTRACT_NAME = 'EscrowReward'

    def fulfill(self,
                agreement_id,
                amounts,
                receivers,
                sender_address,
                lock_condition_id,
                release_condition_id,
                account):
        """
        Fulfill the escrow reward condition.

        :param agreement_id: id of the agreement, hex str
        :param amounts: Array of amount of tokens to distribute, int
        :param receivers: Array of ethereum address of the receivers, hex str
        :param sender_address: ethereum address of the sender, hex str
        :param lock_condition_id: id of the condition, str
        :param release_condition_id: id of the condition, str
        :param account: Account instance
        :return:
        """
        return self._fulfill(
            agreement_id,
            amounts,
            receivers,
            sender_address,
            lock_condition_id,
            release_condition_id,
            transact={'from': account.address,
                      'passphrase': account.password,
                      'keyfile': account.key_file}
        )

    def hash_values(self, amounts, receivers, sender_address, lock_condition_id,
                    release_condition_id):
        """
        Hash the values of the escrow reward condition.

        :param amounts: Array of amount of tokens to distribute, int
        :param receivers: Array of ethereum address of the receivers, hex str
        :param sender_address: ethereum address of the sender, hex str
        :param lock_condition_id: id of the condition, str
        :param release_condition_id: id of the condition, str
        :return: hex str
        """
        return self._hash_values(
            amounts,
            self.to_checksum_addresses(receivers),
            sender_address,
            lock_condition_id,
            release_condition_id
        )

