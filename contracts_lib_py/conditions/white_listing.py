from contracts_lib_py.conditions.condition_base import ConditionBase


class WhitelistingCondition(ConditionBase):
    """Class representing the WhitelistingCondition contract."""
    CONTRACT_NAME = 'WhitelistingCondition'

    def fulfill(self, agreement_id, list_contract_address, address, from_account):
        """
        Fulfill check whether address is whitelisted in order to fulfill the condition.

        :param agreement_id: id of the agreement, hex str
        :param list_contract_address: List contract address, str
        :param address: address in the list, str
        :param from_account: Account instance
        :return: true if the condition was successfully fulfilled, bool
        """
        return self._fulfill(
            agreement_id,
            list_contract_address,
            address,
            transact={'from': from_account.address,
                      'passphrase': from_account.password,
                      'keyfile': from_account.key_file}
        )

    def hash_values(self, list_contract_address, address):
        """
        HashValues generates the hash of condition inputs with the following parameters

        :param list_contract_address: List contract address, str
        :param address: address in the list, str
        :return: hex str
        """
        return self._hash_values(list_contract_address, address)
