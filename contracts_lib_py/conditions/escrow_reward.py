from contracts_lib_py.conditions.condition_base import ConditionBase


class EscrowPaymentCondition(ConditionBase):
    """Class representing the EscrowPaymentCondition contract."""
    CONTRACT_NAME = 'EscrowPaymentCondition'

    def fulfill(self,
                agreement_id,
                did,
                amounts,
                receivers,
                sender_address,
                token_address,
                lock_condition_id,
                release_condition_id,
                account):
        """
        Fulfill the escrow payment condition.

        :param agreement_id: id of the agreement, hex str
        :param did: id of the asset, hex str
        :param amounts: Array of amount of tokens to distribute, int[]
        :param receivers: Array of ethereum address of the receivers, hex str[]
        :param sender_address: ethereum address of the sender, hex str
        :param token_address: the token address to use. If empty  it will use 0x0 address that means ETH payment
        :param lock_condition_id: id of the condition, str
        :param release_condition_id: id of the condition, str
        :param account: Account instance
        :return:
        """
        return self._fulfill(
            agreement_id,
            did,
            amounts,
            self.to_checksum_addresses(receivers),
            sender_address,
            self.validate_token_address(token_address),
            lock_condition_id,
            release_condition_id,
            transact={'from': account.address,
                      'passphrase': account.password,
                      'keyfile': account.key_file}
        )

    def hash_values(self, did, amounts, receivers, sender_address, token_address, lock_condition_id,
                    release_condition_id):
        """
        Hash the values of the escrow reward condition.

        :param did: id of the asset, hex str
        :param amounts: Array of amount of tokens to distribute, int[]
        :param receivers: Array of ethereum address of the receivers, hex str[]
        :param sender_address: ethereum address of the sender, hex str
        :param token_address: the token address to use. If empty  it will use 0x0 address that means ETH payment
        :param lock_condition_id: id of the condition, str
        :param release_condition_id: id of the condition, str
        :return: hex str
        """
        return self._hash_values(
            did,
            amounts,
            self.to_checksum_addresses(receivers),
            sender_address,
            self.validate_token_address(token_address),
            lock_condition_id,
            release_condition_id
        )

