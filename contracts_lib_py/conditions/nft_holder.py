from contracts_lib_py.conditions.condition_base import ConditionBase


class NFTHolderCondition(ConditionBase):
    """Class representing the NFTHolderCondition contract."""
    CONTRACT_NAME = 'NFTHolderCondition'

    def fulfill(self, agreement_id, did, holder_address, amount, account):
        """
        Fulfill the NFT Holder condition.

        :param agreement_id: id of the agreement, hex str
        :param did: refers to the DID in which secret store will issue the decryption
        keys, DID
        :param holder_address: is the address of the user holding the NFT, str
        :param amount: number of NFTs to hold, str
        :param account: Account instance
        :return: true if the condition was successfully fulfilled, bool
        """
        return self._fulfill(
            agreement_id,
            did,
            holder_address,
            amount,
            transact={'from': account.address,
                      'passphrase': account.password,
                      'keyfile': account.key_file}
        )

    def hash_values(self, did, holder_address, amount):
        """
        Hast the values of the document_id with the grantee address.

        :param did: refers to the DID in which secret store will issue the decryption
        keys, DID
        :param holder_address: is the address of the user holding the NFT, str
        :param amount: number of NFTs to hold, str
        :return: hex str
        """
        return self._hash_values(did, holder_address, amount)


