from web3 import Web3

from contracts_lib_py.contract_base import ContractBase


class Token(ContractBase):
    """Class representing the Token contract."""
    CONTRACT_NAME = 'NeverminedToken'

    def get_token_balance(self, account_address):
        """
        Retrieve the amount of tokens of an account address.

        :param account_address: Account address, str
        :return: int
        """
        return self.contract.caller.balanceOf(account_address)

    def get_allowance(self, owner_address, spender_address):
        """

        :param owner_address: Address, str
        :param spender_address: Address, str
        :return:
        """
        return self.contract.caller.allowance(owner_address, spender_address)

    def token_approve(self, spender_address, price, from_account):
        """
        Approve the passed address to spend the specified amount of tokens.

        :param spender_address: Account address, str
        :param price: Asset price, int
        :param from_account: Account address, str
        :return: bool
        """
        if not Web3.isChecksumAddress(spender_address):
            spender_address = Web3.toChecksumAddress(spender_address)

        tx_hash = self.send_transaction(
            'approve',
            (spender_address,
             price),
            transact={'from': from_account.address,
                      'passphrase': from_account.password,
                      'keyfile': from_account.key_file}
        )
        return self.is_tx_successful(tx_hash)

    def transfer(self, receiver_address, amount, from_account):
        """
        Transfer tokens from one account to the receiver address.

        :param receiver_address: Address of the transfer receiver, str
        :param amount: Amount of tokens, int
        :param from_account: Sender account, Account
        :return: bool
        """
        tx_hash = self.send_transaction(
            'transfer',
            (receiver_address,
             amount),
            transact={'from': from_account.address,
                      'passphrase': from_account.password,
                      'keyfile': from_account.key_file}
        )
        return self.is_tx_successful(tx_hash)

    def total_supply(self):
        """
        Return the total supply

        :return: int
        """
        return self.contract.caller.totalSupply()

    def increase_allowance(self, spender_address, added_value, owner_account):
        """

        :param spender_address:
        :param added_value:
        :param owner_account:
        :return: bool
        """
        tx_hash = self.send_transaction(
            'increaseAllowance',
            (spender_address,
             added_value),
            transact={'from': owner_account.address,
                      'passphrase': owner_account.password,
                      'keyfile': owner_account.key_file}
        )
        return self.is_tx_successful(tx_hash)

    def decrease_allowance(self, spender_address, subtracted_value, owner_account):
        """

        :param spender_address:
        :param subtracted_value:
        :param owner_account:
        :return: bool
        """
        tx_hash = self.send_transaction(
            'decreaseAllowance',
            (spender_address,
             subtracted_value),
            transact={'from': owner_account.address,
                      'passphrase': owner_account.password,
                      'keyfile': owner_account.key_file}
        )
        return self.is_tx_successful(tx_hash)
