from contracts_lib_py.conditions.condition_base import ConditionBase


class TransferDIDOwnershipCondition(ConditionBase):
    """Class representing the TransferDIDOwnershipCondition contract."""
    CONTRACT_NAME = 'TransferDIDOwnershipCondition'

    def fulfill(self, agreement_id, did, receiver_address, account):
        """
        Fulfill the access condition.

        :param agreement_id: id of the agreement, hex str
        :param did: refers to the DID in which secret store will issue the decryption
        keys, DID
        :param receiver_address: is the address of the user to receive the DID, str
        :param account: Account instance
        :return: true if the condition was successfully fulfilled, bool
        """
        return self._fulfill(
            agreement_id,
            did,
            receiver_address,
            transact={'from': account.address,
                      'passphrase': account.password,
                      'keyfile': account.key_file}
        )

    def hash_values(self, did, receiver_address):
        """
        Hast the values of the document_id with the grantee address.

        :param did: refers to the DID in which secret store will issue the decryption
        keys, DID
        :param receiver_address: is the address of the user to receive the DID, str
        :return: hex str
        """
        return self._hash_values(did, receiver_address)

