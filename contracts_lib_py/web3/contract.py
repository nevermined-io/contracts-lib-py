import logging

from web3._utils import empty
from web3.contract import prepare_transaction

from contracts_lib_py.wallet import Wallet


class CustomContractFunction:

    def __init__(self, contract_function):
        self._contract_function = contract_function

    def transact(self, transaction=None):
        """
        Customize calling smart contract transaction functions to use `sendTransaction`
        instead of `eth_sendTransaction` and to estimate gas limit. This function
        is largely copied from web3 ContractFunction with important addition.

        Note: will fallback to `eth_sendTransaction` if `passphrase` is not provided in the
        `transaction` dict.

        :param transaction: dict which has the required transaction arguments per
            `sendTransaction` requirements.
        :return: hex str transaction hash
        """
        if transaction is None:
            transact_transaction = {}
        else:
            transact_transaction = dict(**transaction)

        if 'data' in transact_transaction:
            raise ValueError("Cannot set data in transact transaction")

        cf = self._contract_function
        if cf.address is not None:
            transact_transaction.setdefault('to', cf.address)
        if cf.web3.eth.defaultAccount is not empty:
            transact_transaction.setdefault('from', cf.web3.eth.defaultAccount)

        if 'to' not in transact_transaction:
            if isinstance(self, type):
                raise ValueError(
                    "When using `Contract.transact` from a contract factory you "
                    "must provide a `to` address with the transaction"
                )
            else:
                raise ValueError(
                    "Please ensure that this contract instance has an address."
                )

        if 'gas' not in transact_transaction:
            tx = transaction.copy()
            if 'passphrase' in tx:
                tx.pop('passphrase')
            if 'keyfile' in tx:
                tx.pop('keyfile')
            gas = cf.estimateGas(tx)
            transact_transaction['gas'] = gas

        return transact_with_contract_function(
            cf.address,
            cf.web3,
            cf.function_identifier,
            transact_transaction,
            cf.contract_abi,
            cf.abi,
            *cf.args,
            **cf.kwargs
        )


def transact_with_contract_function(
        address,
        web3,
        function_name=None,
        transaction=None,
        contract_abi=None,
        fn_abi=None,
        *args,
        **kwargs):
    """
    Helper function for interacting with a contract function by sending a
    transaction. This is copied from web3 `transact_with_contract_function`
    so we can use `personal_sendTransaction` when possible.
    """
    transact_transaction = prepare_transaction(
        address,
        web3,
        fn_identifier=function_name,
        contract_abi=contract_abi,
        transaction=transaction,
        fn_abi=fn_abi,
        fn_args=args,
        fn_kwargs=kwargs,
    )

    passphrase = None
    key_file = None
    if transaction and 'passphrase' in transaction:
        passphrase = transaction['passphrase']
        transact_transaction.pop('passphrase')
        if 'keyfile' in transaction:
            key_file = transaction['keyfile']
            transact_transaction.pop('keyfile')

    # Restrict transactions to raw transactions for now (security first)
    # if not (passphrase and key_file):
    #     raise AssertionError(
    #         'password and key file are required for signing transactions locally.'
    #     )

    if passphrase and key_file:
        raw_tx = Wallet(web3, key_file, passphrase).sign_tx(transact_transaction)
        logging.debug(f'sending raw tx: function: {function_name}, tx hash: {raw_tx.hex()}')
        txn_hash = web3.eth.sendRawTransaction(raw_tx)
    elif passphrase:
        txn_hash = web3.sendTransaction(transact_transaction, passphrase)
    else:
        txn_hash = web3.eth.sendTransaction(transact_transaction)

    return txn_hash
