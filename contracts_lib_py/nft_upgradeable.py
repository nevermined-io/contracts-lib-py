from web3 import Web3

from contracts_lib_py.contract_base import ContractBase


class NFTUpgradeable(ContractBase):
    """Class representing the NFTUpgradeable contract."""
    CONTRACT_NAME = 'NFTUpgradeable'

    def is_approved_for_all(self, account_address, operator_address):
        """
        Retrieves if the operator is approved for an account adress

        :param account_address: Account address, str
        :param operator_address: Account address, str
        :return: bool
        """
        return self.contract.caller.isApprovedForAll(
            Web3.toChecksumAddress(account_address),
            Web3.toChecksumAddress(operator_address)
        )

    def set_proxy_approval(self, operator_address, approved, from_account):
        """
        Configure proxy approval for a specific operator address

        :param operator_address: Address of the operator, str
        :param approved: is approved, bool
        :param from_account: Sender account, Account
        :return: bool
        """
        tx_hash = self.send_transaction(
            'setProxyApproval',
            (Web3.toChecksumAddress(operator_address),
             approved),
            transact={'from': from_account.address,
                      'passphrase': from_account.password,
                      'keyfile': from_account.key_file}
        )
        return self.is_tx_successful(tx_hash)

    def proxy_set_approval_for_all(self, account_address, operator_address, approved, from_account):
        """
        Configure proxy approval for a specific account and operator address

        :param account_address: Address of the account, str
        :param operator_address: Address of the operator, str
        :param approved: is approved, bool
        :param from_account: Sender account, Account
        :return: bool
        """
        tx_hash = self.send_transaction(
            'proxySetApprovalForAll',
            (Web3.toChecksumAddress(account_address),
             Web3.toChecksumAddress(operator_address),
             approved),
            transact={'from': from_account.address,
                      'passphrase': from_account.password,
                      'keyfile': from_account.key_file}
        )
        return self.is_tx_successful(tx_hash)

    def set_approval_for_all(self, operator_address, approved, from_account):
        """
        Configure approval for a specific operator address

        :param operator_address: Address of the operator, str
        :param approved: is approved, bool
        :param from_account: Sender account, Account
        :return: bool
        """
        tx_hash = self.send_transaction(
            'setApprovalForAll',
            (Web3.toChecksumAddress(operator_address),
             approved),
            transact={'from': from_account.address,
                      'passphrase': from_account.password,
                      'keyfile': from_account.key_file}
        )
        return self.is_tx_successful(tx_hash)

    def mint(self, to_address, did, amount, data, from_account):
        """
        Mint NFTs

        :param to_address: Address of the receiver, str
        :param did: identifier of the asset, str
        :param amount: number of nfts to mint, uint
        :param data: additional data, str
        :param from_account: Sender account, Account
        :return: bool
        """
        tx_hash = self.send_transaction(
            'mint',
            (Web3.toChecksumAddress(to_address),
             int(did, 16),
             amount,
             data),
            transact={'from': from_account.address,
                      'passphrase': from_account.password,
                      'keyfile': from_account.key_file}
        )
        return self.is_tx_successful(tx_hash)

    def burn(self, to_address, did, amount, from_account):
        """
        Burn NFTs

        :param to_address: Address, str
        :param did: identifier of the asset, str
        :param amount: number of nfts to burn, uint
        :param from_account: Sender account, Account
        :return: bool
        """
        tx_hash = self.send_transaction(
            'burn',
            (Web3.toChecksumAddress(to_address),
             int(did, 16),
             amount),
            transact={'from': from_account.address,
                      'passphrase': from_account.password,
                      'keyfile': from_account.key_file}
        )
        return self.is_tx_successful(tx_hash)

    def add_minter(self, account_address, from_account):
        """
        Add an account as minter

        :param account_address: Account address, str
        :param from_account: Account address, str
        :return: bool
        """
        tx_hash = self.send_transaction(
            'addMinter',
            Web3.toChecksumAddress(account_address),
            transact={'from': from_account.address,
                      'passphrase': from_account.password,
                      'keyfile': from_account.key_file}
        )
        return self.is_tx_successful(tx_hash)

    def balance(self, address, did):
        """
        Returns the NFT balance for an address

        :param address: Account address to check, str
        :param did: The NFT id, str
        :return: int
        """
        return self.contract.caller.balanceOf(address, int(did, 16))

    def transfer_nft(self, did, address, amount, account):
        tx_hash = self.send_transaction(
            'safeTransferFrom',
            (account.address,
             address,
             int(did, 16),
             amount,
             Web3.toBytes(text='')
             ),
            transact={'from': account.address,
                      'passphrase': account.password,
                      'keyfile': account.key_file}
        )
        return self.is_tx_successful(tx_hash)