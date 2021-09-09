from contracts_lib_py.conditions.condition_base import ConditionBase

class AccessProofCondition(ConditionBase):
    """Class representing the AccessProofCondition contract."""
    CONTRACT_NAME = 'AccessProofCondition'

    def fulfill(self, agreement_id, hash, buyer, provider, cipher, proof, account):
        """
        Fulfill the access condition.

        :param agreement_id: id of the agreement, hex str
        :param document_id: refers to the DID in which secret store will issue the decryption
        keys, DID
        :param grantee_address: is the address of the granted user, str
        :param account: Account instance
        :return: true if the condition was successfully fulfilled, bool
        """
        return self._fulfill(
            agreement_id,
            hash,
            buyer,
            provider,
            cipher,
            proof,
            transact={'from': account.address,
                      'passphrase': account.password,
                      'keyfile': account.key_file}
        )

    def hash_values(self, hash, buyer, provider):
        """
        Hast the values of the document_id with the grantee address.

        :param document_id: refers to the DID in which secret store will issue the decryption
        keys, DID
        :param grantee_address: is the address of the granted user, str
        :return: hex str
        """
        return self._hash_values(hash, buyer, provider)

