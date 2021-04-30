from contracts_lib_py.conditions.condition_base import ConditionBase

class NFTLockCondition(ConditionBase):
    """Class representing the NFTLockCondition contract."""
    CONTRACT_NAME = 'NFTLockCondition'

    def fulfill(self, agreement_id, document_id, reward_address, amount, account):
        """
        Fulfill the nft lock condition.

        :param agreement_id: id of the agreement, hex str
        :param document_id: refers to the DID in which secret store will issue the decryption
        keys, DID
        :param reward_address: is the contract address where the reward is locked, str
        :param amount: is the amount of tokens to be transfered, int
        :param account: Account instance
        :return: true if the condition was successfully fulfilled, bool
        """
        return self._fulfill(
            agreement_id,
            document_id,
            reward_address,
            amount,
            transact={'from': account.address,
                      'passphrase': account.password,
                      'keyfile': account.key_file}
        )

    def hash_values(self, document_id, reward_address, amount):
        """
        Hash the values of the document_id with the reward_address and amount.

        :param document_id: refers to the DID in which secret store will issue the decryption
        keys, DID
        :param reward_address: is the final address to receive the NFTs, str
        :param amount: is the amount of locked tokens, int
        :return: hex str
        """
        return self._hash_values(document_id, reward_address, amount)