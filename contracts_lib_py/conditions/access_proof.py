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
        print([agreement_id, hash, buyer, provider, cipher])
        return self._fulfill(
            agreement_id,
            int(hash, 16),
            [int(buyer[0], 16), int(buyer[1], 16)],
            [int(provider[0], 16), int(provider[1], 16)],
            [int(cipher[0], 16), int(cipher[1], 16)],
            bytes.fromhex(proof[2:]),
            transact={'from': account.address,
                      'passphrase': account.password,
                      'gas': 2000000,
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
        res = self._hash_values(int(hash, 16), [int(buyer[0], 16), int(buyer[1], 16)], [int(provider[0], 16), int(provider[1], 16)])
        print('hashed result')
        print(res)
        return res

