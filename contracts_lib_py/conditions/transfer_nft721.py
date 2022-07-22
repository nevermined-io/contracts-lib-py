from contracts_lib_py.conditions.condition_base import ConditionBase


class TransferNFT721Condition(ConditionBase):
    """Class representing the TransferNFTCondition contract."""
    CONTRACT_NAME = 'TransferNFT721Condition'

    def fulfill(self, agreement_id, did, receiver_address, nft_amount, lock_cond_id, nft_contract_address, transfer, account):
        """
        Fulfill the NFT Holder condition.

        :param agreement_id: id of the agreement, hex str
        :param did: refers to the DID in which secret store will issue the decryption
        keys, DID
        :param receiver_address: is the address of the user to receive the NFT, str
        :param nft_amount: number of NFTs to hold, str
        :param lock_cond_id: Lock Condition Identifier, str
        :param nft_contract_address: The address of the NFT Contract to use, str
        :param transfer if yes it does a transfer if false it mints the NFT, bool
        :param account: Account instance
        :return: true if the condition was successfully fulfilled, bool
        """
        return self._fulfill(
            agreement_id,
            did,
            receiver_address,
            nft_amount,
            lock_cond_id,
            nft_contract_address,
            transfer,
            transact={'from': account.address,
                      'passphrase': account.password,
                      'keyfile': account.key_file}
        )

    def fulfill_for_delegate(self, agreement_id, did, nft_holder_address, receiver_address, nft_amount, lock_cond_id,
                             transfer, nft_contract_address, duration, account):
        """
        Fulfill the NFT Holder condition.

        :param agreement_id: id of the agreement, hex str
        :param did: refers to the DID in which secret store will issue the decryption
        keys, DID
        :param nft_holder_address: is the address of the user holding the NFT, str
        :param receiver_address: is the address of the user to receive the NFT, str
        :param nft_amount: number of NFTs to hold, str
        :param lock_cond_id: Lock Condition Identifier, str
        :param transfer if yes it does a transfer if false it mints the NFT, bool
        :param nft_contract_address the address of the ERC-721
        :param duration number of blocks of duration of the subscription, int
        :param account: Account instance
        :return: true if the condition was successfully fulfilled, bool
        """

        if duration > 0:
            duration = duration + Web3Provider.get_web3().eth.get_block_number()
        return self._fulfill(
            agreement_id,
            did,
            nft_holder_address,
            receiver_address,
            nft_amount,
            lock_cond_id,
            transfer,
            nft_contract_address,
            duration,
            method='fulfillForDelegate',
            transact={'from': account.address,
                      'passphrase': account.password,
                      'keyfile': account.key_file,
                      'gas': 1000000}
        )

    def hash_values(self, did, nft_holder, receiver_address, nft_amount, lock_cond_id, nft_contract_address, transfer):
        """
        Hast the values of the document_id with the grantee address.

        :param did: refers to the DID in which secret store will issue the decryption
        keys, DID
        :param nft_holder: The current older of the nft
        :param receiver_address: is the address of the user to receive the NFT, str
        :param nft_amount: number of NFTs, str
        :param lock_cond_id: Lock Condition Identifier, str
        :param nft_contract_address: The address of the NFT Contract to use
        :param transfer if yes it does a transfer if false it mints the NFT, bool
        :return: hex str
        """
        return self._hash_values(did, nft_holder, receiver_address, nft_amount, lock_cond_id, nft_contract_address, transfer)

    def get_nft_default_address(self):
        """
        Returns the default NFT Contract used in the Transfer Condition

        :return: nft contract address
        """
        return self._get_nft_default_address()

