from contracts_lib_py.conditions.condition_base import ConditionBase
from contracts_lib_py.event_filter import EventFilter


class TransferNFTCondition(ConditionBase):
    """Class representing the TransferNFTCondition contract."""
    CONTRACT_NAME = 'TransferNFTCondition'

    def fulfill(self, agreement_id, did, receiver_address, nft_amount, lock_cond_id, account):
        """
        Fulfill the NFT Holder condition.

        :param agreement_id: id of the agreement, hex str
        :param did: refers to the DID in which secret store will issue the decryption
        keys, DID
        :param receiver_address: is the address of the user to receive the NFT, str
        :param nft_amount: number of NFTs to hold, str
        :param lock_cond_id: Lock Condition Identifier, str
        :param account: Account instance
        :return: true if the condition was successfully fulfilled, bool
        """
        return self._fulfill(
            agreement_id,
            did,
            receiver_address,
            nft_amount,
            lock_cond_id,
            transact={'from': account.address,
                      'passphrase': account.password,
                      'keyfile': account.key_file}
        )

    def hash_values(self, did, nft_holder, receiver_address, nft_amount, lock_cond_id):
        """
        Hast the values of the document_id with the grantee address.

        :param did: refers to the DID in which secret store will issue the decryption
        keys, DID
        :param nft_holder: The current older of the nft
        :param receiver_address: is the address of the user to receive the NFT, str
        :param nft_amount: number of NFTs, str
        :param lock_cond_id: Lock Condition Identifier, str
        :return: hex str
        """
        return self._hash_values(did, nft_holder, receiver_address, nft_amount, lock_cond_id)


