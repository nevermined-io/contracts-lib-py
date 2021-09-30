import logging
from collections import namedtuple
from urllib.parse import urlparse

from eth_utils import add_0x_prefix
from web3 import Web3
from web3._utils.events import get_event_data

from contracts_lib_py.contract_base import ContractBase
from contracts_lib_py.event_filter import EventFilter
from contracts_lib_py.exceptions import DIDNotFound
from contracts_lib_py.web3_provider import Web3Provider

logger = logging.getLogger(__name__)

DIDRegisterValues = namedtuple(
    'DIDRegisterValues',
    ('owner', 'last_checksum', 'url', 'last_updated_by', 'block_number_updated', 'providers',
     'nft_supply', 'mint_cap', 'royalties')
)


class DIDRegistry(ContractBase):
    """Class to register and update DID's."""
    DID_REGISTRY_EVENT_NAME = 'DIDAttributeRegistered'
    PROVENANCE_ATTRIBUTE_REGISTERED_EVENT_NAME = 'ProvenanceAttributeRegistered'
    PROVENANCE_USED_EVENT_NAME = 'Used'
    PROVENANCE_WAS_GENERATED_BY_EVENT_NAME = 'WasGeneratedBy'
    PROVENANCE_WAS_DERIVED_FROM_EVENT_NAME = 'WasDerivedFrom'
    PROVENANCE_WAS_ASSOCIATED_WITH_EVENT_NAME = 'WasAssociatedWith'
    PROVENANCE_ACTED_ON_BEHALF_EVENT_NAME = 'ActedOnBehalf'

    CONTRACT_NAME = 'DIDRegistry'

    def register_mintable_did(self, did_seed, checksum, url, cap, royalties, account, providers=None, activity_id=None,
                              attributes=None):
        """
        Register a mintable DID using the DIDRegistry smart contract.

        :param did_seed: Seed used to generate the final DID, It's a 32 byte or hexstring
        :param checksum: hex str hash of TODO
        :param url: URL of the resolved DID
        :param account: instance of Account to use to register/update the DID
        :param cap: refers to the mint cap
        :param royalties: refers to the royalties to reward to the DID creator in the secondary market
        :param providers: list of addresses of providers to be allowed to serve the asset and play
            a part in creating and fulfilling service agreements
        :param activity_id: id of the activity tracked in the provenance.
        :param attributes: additional provenance attributes
        :return: Receipt
        """
        return self.register(did_seed, checksum, url, account,
                             cap=cap, royalties=royalties, attributes=attributes,
                             providers=providers, activity_id=activity_id)

    def register(self, did_seed, checksum, url, account, providers=None, activity_id=None,
                 attributes=None, cap=None, royalties=None):
        """
        Register or update a DID on the block chain using the DIDRegistry smart contract.

        :param did_seed: Seed used to generate the final DID, It's a 32 byte or hexstring
        :param checksum: hex str hash of TODO
        :param url: URL of the resolved DID
        :param account: instance of Account to use to register/update the DID
        :param providers: list of addresses of providers to be allowed to serve the asset and play
            a part in creating and fulfilling service agreements
        :param activity_id: id of the activity tracked in the provenance.
        :param cap: refers to the mint cap
        :param royalties: refers to the royalties to reward to the DID creator in the secondary market
        :param attributes: additional provenance attributes
        :return: Receipt
        """
        if isinstance(did_seed, bytes):
            did_source_id = did_seed
        elif isinstance(did_seed, str):
            try:
                did_source_id = Web3.toBytes(hexstr=did_seed)
            except Exception as e:
                raise TypeError(
                    f'There is a problem with the did type, expecting a str with valid hex only, '
                    f'got {did_seed}. Make sure to use only the id part of the '
                    f'did without the prefix: {e}')
        else:
            raise TypeError(f'Unrecognized `did_seed` {did_seed} of type {type(did_seed)}. Expecting a 32 bytes '
                            f'in bytes type or hex str representation.')

        if not did_source_id:
            raise ValueError(f'{did_seed} must be a valid DID to register')

        if not urlparse(url):
            raise ValueError(f'Invalid URL {url} to register for DID {did_seed}')

        if checksum is None:
            checksum = Web3.toBytes(0)

        if not isinstance(checksum, bytes):
            raise ValueError(f'Invalid checksum value {checksum}, must be bytes or string')

        if account is None:
            raise ValueError('You must provide an account to use to register a DID')

        if cap is not None or royalties is not None:
            transaction = self._register_mintable_did(
                did_source_id, checksum, providers or [], url, account, cap, royalties, activity_id, attributes
            )
        else:
            transaction = self._register_did(
                did_source_id, checksum, providers or [], url, account, activity_id, attributes
            )
        receipt = self.get_tx_receipt(transaction)
        if receipt:
            return receipt.status == 1

        did = self.hash_did(did_source_id, account.address)

        _filters = dict()
        _filters['_did'] = Web3.toBytes(hexstr=did)
        _filters['_owner'] = Web3.toBytes(hexstr=account.address)
        event = self.subscribe_to_event(self.DID_REGISTRY_EVENT_NAME, 15, _filters, wait=True)
        return event is not None

    def hash_did(self, did_seed, address):
        """
        Calculates the final DID given a DID seed and the publisher address
        :param did_seed: the hash used to generate the did
        :param address: the address of the account creating the asset
        :return: the final DID
        """
        return add_0x_prefix(self.contract.caller.hashDID(did_seed, address).hex())

    def are_royalties_valid(self, did, amounts, receivers):
        """
        Validates if asset royalties are valid
        :param did:  Asset did, did
        :param amounts: amounts to distribute
        :param receivers: receivers of the amounts
        :return: boolean
        """
        return self.contract.caller.areRoyaltiesValid(did, amounts, receivers)

    def get_block_number_updated(self, did):
        """Return the block number the last did was updated on the block chain."""
        return self.contract.caller.getBlockNumberUpdated(did)

    def get_did_owner(self, did):
        """
        Return the owner of the did.

        :param did: Asset did, did
        :return: ethereum address, hex str
        """
        return self.contract.caller.getDIDOwner(did)

    def add_provider(self, did, provider_address, account):
        """
        Add the provider of the did.

        :param did: the id of an asset on-chain, hex str
        :param provider_address: ethereum account address of the provider, hex str
        :param account: Account executing the action
        :return:
        """
        tx_hash = self.send_transaction(
            'addDIDProvider',
            (did,
             provider_address),
            transact={'from': account.address,
                      'passphrase': account.password,
                      'keyfile': account.key_file}
        )
        return self.is_tx_successful(tx_hash)

    def remove_provider(self, did, provider_address, account):
        """
        Remove a provider

        :param did: the id of an asset on-chain, hex str
        :param provider_address: ethereum account address of the provider, hex str
        :param account: Account executing the action
        :return:
        """
        tx_hash = self.send_transaction(
            'removeDIDProvider',
            (did,
             provider_address),
            transact={'from': account.address,
                      'passphrase': account.password,
                      'keyfile': account.key_file}
        )
        return self.is_tx_successful(tx_hash)

    def transfer_did_ownership(self, did, new_owner_address, account):
        """
        Transfer did ownership to an address.

        :param did: the id of an asset on-chain, hex str
        :param new_owner_address: ethereum account address, hex str
        :param account: Account executing the action
        :return: bool
        """
        tx_hash = self.send_transaction(
            'transferDIDOwnership',
            (did, new_owner_address),
            transact={'from': account.address,
                      'passphrase': account.password,
                      'keyfile': account.key_file}
        )
        return self.is_tx_successful(tx_hash)

    def grant_permission(self, did, address_to_grant, account):
        """
        Grant access permission to an address.

        :param did: the id of an asset on-chain, hex str
        :param address_to_grant: ethereum account address, hex str
        :param account: Account executing the action
        :return: bool
        """
        tx_hash = self.send_transaction(
            'grantPermission',
            (did, address_to_grant),
            transact={'from': account.address,
                      'passphrase': account.password,
                      'keyfile': account.key_file}
        )
        return self.is_tx_successful(tx_hash)

    def revoke_permission(self, did, address_to_revoke, account):
        """
        Revoke access permission to an address.

        :param did: the id of an asset on-chain, hex str
        :param address_to_revoke: ethereum account address, hex str
        :param account: Account executing the action
        :return: bool
        """
        tx_hash = self.send_transaction(
            'revokePermission',
            (did, address_to_revoke),
            transact={'from': account.address,
                      'passphrase': account.password,
                      'keyfile': account.key_file}
        )
        return self.is_tx_successful(tx_hash)

    def get_permission(self, did, address):
        """
        Gets access permission of a grantee

        :param did: the id of an asset on-chain, hex str
        :param address: ethereum account address, hex str
        :return: true if the address has access permission to a DID
        """
        return self.contract.caller.getPermission(did, address)

    def is_did_provider(self, did, address):
        """
        Return true if the address is the Provider of the did.

        :param did: the id of an asset on-chain, hex str
        :param address: ethereum account address, hex str
        :return: bool
        """
        return self.contract.caller.isDIDProvider(did, address)

    def get_did_providers(self, did):
        """
        Return the list providers registered on-chain for the given did.

        :param did: hex str the id of an asset on-chain
        :return:
            list of addresses
            None if asset has no registerd providers
        """
        register_values = self.contract.caller.getDIDRegister(did)
        print(register_values)
        if register_values and len(register_values) >= 6 and register_values[0]:
            # sanitize providers list, because if providers were removed they will
            # be replaced with null/None
            valid_providers = [a for a in register_values[5] if
                               a != '0x0000000000000000000000000000000000000000']
            register_values[5] = valid_providers
            return DIDRegisterValues(*register_values).providers

    def get_owner_asset_ids(self, address):
        """
        Get the list of assets owned by an address owner.

        :param address: ethereum account address, hex str
        :return:
        """
        block_filter = self._get_event_filter(DIDRegistry.DID_REGISTRY_EVENT_NAME, owner=address)
        log_items = block_filter.get_all_entries(max_tries=5)
        did_list = []
        for log_i in log_items:
            did_list.append(log_i.args['_did'])

        return did_list

    def get_registered_attribute(self, did_bytes):
        """

        Example of event logs from event_filter.get_all_entries():
        [AttributeDict(
            {'args': AttributeDict(
                {'did': b'\x02n\xfc\xfb\xfdNM\xe9\xb8\xe0\xba\xc2\xb2\xc7\xbeg\xc9/\x95\xc3\x16\
                           x98G^\xb9\xe1\xf0T\xce\x83\xcf\xab',
                 'owner': '0xAd12CFbff2Cb3E558303334e7e6f0d25D5791fc2',
                 'value': 'http://localhost:5000',
                 'checksum': '0x...',
                 'updatedAt': 1947}),
             'event': 'DIDAttributeRegistered',
             'logIndex': 0,
             'transactionIndex': 1,
             'transactionHash': HexBytes(
             '0xea9ca5748d54766fb43fe9660dd04b2e3bb29a0fbe18414457cca3dd488d359d'),
             'address': '0x86DF95937ec3761588e6DEbAB6E3508e271cC4dc',
             'blockHash': HexBytes(
             '0xbbbe1046b737f33b2076cb0bb5ba85a840c836cf1ffe88891afd71193d677ba2'),
             'blockNumber': 1947})]

        """
        result = None
        did = Web3.toHex(did_bytes)
        block_number = self.get_block_number_updated(did_bytes)
        logger.debug(f'got blockNumber {block_number} for did {did}')
        if block_number == 0:
            raise DIDNotFound(
                f'DID "{did}" is not found on-chain in the current did registry. '
                f'Please ensure assets are registered in the correct keeper contracts. '
                f'The keeper-contracts DIDRegistry address is {self.address}.'
                f'Also ensure that sufficient time has passed after registering the asset '
                f'such that the transaction is confirmed by the network validators.')

        events = Web3Provider.get_web3().eth.getLogs({
            'fromBlock': block_number,
            'toBlock': block_number,
            'address': self.contract.address
        })
        event_data = self._filter_did_registered_events(did_bytes, events)

        if event_data:
            result = {
                'checksum': event_data.args._checksum,
                'value': event_data.args._value,
                'block_number': block_number,
                'did_bytes': event_data.args._did,
                'owner': Web3.toChecksumAddress(event_data.args._owner),
            }
        else:
            logger.warning(f'Could not find {DIDRegistry.DID_REGISTRY_EVENT_NAME} event logs for '
                           f'did {did} at blockNumber {block_number}')
        return result

    def _filter_did_registered_events(self, did_bytes, events):
        # https://ethereum.stackexchange.com/a/106981/3831

        event_template = getattr(self.contract.events, DIDRegistry.DID_REGISTRY_EVENT_NAME)
        for event in events:
            try:
                event_data  = get_event_data(event_template.web3.codec, event_template._get_event_abi(), event)
                if event_data['args']['_did'] == did_bytes:
                    return event_data
            except Exception:
                continue


    def _register_did(self, did, checksum, providers, url, account, activity_id=None,
                      attributes=None):
        assert isinstance(providers, list), ''
        return self.send_transaction(
            'registerDID',
            (did,
             checksum,
             providers,
             url,
             activity_id or '',
             attributes or ''),
            transact={'from': account.address,
                      'passphrase': account.password,
                      'keyfile': account.key_file}
        )

    def _register_mintable_did(self, did, checksum, providers, url, account, cap, royalties, activity_id=None,
                               attributes=None):
        assert isinstance(providers, list), ''
        return self.send_transaction(
            'registerMintableDID',
            (did,
             checksum,
             providers,
             url,
             cap,
             royalties,
             activity_id or '',
             attributes or ''),
            transact={'from': account.address,
                      'passphrase': account.password,
                      'keyfile': account.key_file}
        )

    def used(self, prov_id, did, agent_id, activity_id, signature, account, attributes=None):
        tx_hash = self.send_transaction(
            'used',
            (prov_id,
             did,
             agent_id,
             activity_id,
             signature,
             attributes),
            transact={'from': account.address,
                      'passphrase': account.password,
                      'keyfile': account.key_file}
        )

        return Web3Provider.get_web3().eth.waitForTransactionReceipt(tx_hash, timeout=20)

    def was_derived_from(self, prov_id, new_entity_did, used_entity_did, agent_id, activity_id,
                         account, attributes=None):
        tx_hash = self.send_transaction(
            'wasDerivedFrom',
            (prov_id,
             new_entity_did,
             used_entity_did,
             agent_id,
             activity_id,
             attributes),
            transact={'from': account.address,
                      'passphrase': account.password,
                      'keyfile': account.key_file}
        )

        return Web3Provider.get_web3().eth.waitForTransactionReceipt(tx_hash, timeout=20)

    def was_associated_with(self, prov_id, did, agent_id, activity_id,
                            account, attributes=None):
        tx_hash = self.send_transaction(
            'wasAssociatedWith',
            (prov_id,
             did,
             agent_id,
             activity_id,
             attributes),
            transact={'from': account.address,
                      'passphrase': account.password,
                      'keyfile': account.key_file}
        )
        return Web3Provider.get_web3().eth.waitForTransactionReceipt(tx_hash, timeout=20)

    def acted_on_behalf(self, prov_id, did, delegate_agent_id, responsible_agent_id, activity_id,
                        signature, account, attributes=None):
        tx_hash = self.send_transaction(
            'actedOnBehalf',
            (prov_id,
             did,
             delegate_agent_id,
             responsible_agent_id,
             activity_id,
             signature,
             attributes),
            transact={'from': account.address,
                      'passphrase': account.password,
                      'keyfile': account.key_file}
        )
        return Web3Provider.get_web3().eth.waitForTransactionReceipt(tx_hash, timeout=20)

    def add_did_provenance_delegate(self, did, delegate, account):
        tx_hash = self.send_transaction(
            'addDIDProvenanceDelegate',
            (did,
             delegate),
            transact={'from': account.address,
                      'passphrase': account.password,
                      'keyfile': account.key_file}
        )
        return self.is_tx_successful(tx_hash)

    def remove_did_provenance_delegate(self, did, delegate, account):
        tx_hash = self.send_transaction(
            'removeDIDProvenanceDelegate',
            (did,
             delegate),
            transact={'from': account.address,
                      'passphrase': account.password,
                      'keyfile': account.key_file}
        )
        return self.is_tx_successful(tx_hash)

    def is_provenance_delegate(self, did, delegate):
        return self.contract.caller.isProvenanceDelegate(did, delegate)

    def get_provenance_owner(self, did):
        return self.contract.caller.getProvenanceOwner(did)

    def is_provenance_signature_correct(self, agent_id, hash, signature):
        return self.contract.caller.provenanceSignatureIsCorrect(agent_id, hash, signature)

    def get_did_register(self, did):
        entry = self.contract.caller.getDIDRegister(did)
        valid_providers = [a for a in entry[5] if a != '0x0000000000000000000000000000000000000000']
        return {
            'owner': entry[0],
            'lastChecksum': entry[1],
            'url': entry[2],
            'lastUpdatedBy': entry[3],
            'blockNumberUpdated': entry[4],
            'providers': valid_providers,
            'nftSupply': entry[6],
            'mintCap': entry[7],
            'royalties': entry[8]
        }

    def get_provenance_entry(self, prov_id):
        provenance_entry = self.contract.caller.getProvenanceEntry(prov_id)
        return {'did': Web3.toHex(provenance_entry[0]),
                'related_did': Web3.toHex(provenance_entry[1]),
                'agent_id': provenance_entry[2],
                'activity_id': Web3.toHex(provenance_entry[3]),
                'agent_involved_id': provenance_entry[4],
                'method': provenance_entry[5],
                'created_by': provenance_entry[6],
                'block_number_updated': provenance_entry[7],
                'signature': provenance_entry[8]
                }

    def get_did_provenance_events(self, did_bytes):
        result = []
        did = Web3.toHex(did_bytes)
        block_filter = self._get_event_filter(
            DIDRegistry.PROVENANCE_ATTRIBUTE_REGISTERED_EVENT_NAME,
            did=did,
            from_block=0,
            to_block='latest')
        log_items = block_filter.get_all_entries(max_tries=5)
        if log_items:
            for i in range(len(log_items)):
                log_item = log_items[i].args
                block_number = log_item['_blockNumberUpdated']
                result.append({
                    'prov_id': log_item['provId'],
                    'did_bytes': log_item['_did'],
                    'agent_id': Web3.toChecksumAddress(log_item['_agentId']),
                    'activity_id': log_item['_activityId'],
                    'method': log_item['_method'],
                    'related_did': log_item['_relatedDid'],
                    'agent_involvedId': log_item['_agentInvolvedId'],
                    'attributes': log_item['_attributes'],
                    'block_number': block_number,

                })
        else:
            logger.warning(
                f'Could not find {DIDRegistry.PROVENANCE_ATTRIBUTE_REGISTERED_EVENT_NAME} event '
                f'logs for '
                f'did {did} at blockNumber ')
        return result

    def get_provenance_method_events(self, method, did_bytes):
        result = []
        did = Web3.toHex(did_bytes)
        try:
            event_name = self._method_mapper(method)
        except Exception as e:
            raise Exception(f'Provenance mapping exception: {e}')
        block_filter = self._get_event_filter(
            event_name,
            did=did
        )
        log_items = block_filter.get_all_entries(max_tries=5)
        if log_items:
            for i in range(len(log_items)):
                log_item = log_items[i].args
                block_number = log_item['_blockNumberUpdated']
                result.append({
                    'prov_id': log_item['provId'],
                    'did_bytes': did_bytes,
                    'agent_id': log_item.get('_agentId', None),
                    'activity_id': log_item['_activityId'],
                    'method': method,
                    'related_did': log_item.get('_relatedDid', None),
                    'agent_involvedId': log_item.get('_agentInvolvedId', None),
                    'attributes': log_item['_attributes'],
                    'block_number': block_number,

                })
        else:
            logger.warning(
                f'Could not find {DIDRegistry.PROVENANCE_ATTRIBUTE_REGISTERED_EVENT_NAME} event '
                f'logs for '
                f'did {did} at blockNumber')
        return result

    def mint(self, did, amount, account):
        tx_hash = self.send_transaction(
            'mint',
            (did, amount),
            transact={'from': account.address,
                      'passphrase': account.password,
                      'keyfile': account.key_file}
        )

        return self.is_tx_successful(tx_hash)

    def burn(self, did, amount, account):
        tx_hash = self.send_transaction(
            'burn',
            (did, amount),
            transact={'from': account.address,
                      'passphrase': account.password,
                      'keyfile': account.key_file}
        )
        return self.is_tx_successful(tx_hash)

    def balance(self, address, did):
        return self.contract.caller.balanceOf(address, did)

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

    def is_nft_approved_for_all(self, account, operator):
        """
        Return true if the operator address is ERC1155 approved

        :param account: the account address to check, hex str
        :param operator: ethereum operator address, hex str
        :return: bool
        """
        return self.contract.caller.isApprovedForAll(account, operator)

    def set_nft_proxy_approval(self, operator, approved, account):
        tx_hash = self.send_transaction(
            'setProxyApproval',
            (operator, approved),
            transact={'from': account.address,
                      'passphrase': account.password,
                      'keyfile': account.key_file}
        )
        return self.is_tx_successful(tx_hash)


    def _get_event_filter(self, event_name, did=None, owner=None, from_block=0, to_block='latest'):
        _filters = {}
        if event_name == DIDRegistry.PROVENANCE_WAS_DERIVED_FROM_EVENT_NAME:
            _filters['_newEntityDid'] = Web3.toBytes(hexstr=did)
        elif event_name == DIDRegistry.PROVENANCE_WAS_ASSOCIATED_WITH_EVENT_NAME or event_name == DIDRegistry.PROVENANCE_ACTED_ON_BEHALF_EVENT_NAME:
            _filters['_entityDid'] = Web3.toBytes(hexstr=did)
        else:
            if did is not None:
                _filters['_did'] = Web3.toBytes(hexstr=did)
            if owner is not None:
                _filters['_owner'] = Web3.toBytes(hexstr=owner)

        block_filter = EventFilter(
            event_name,
            getattr(self.events, event_name),
            from_block=from_block,
            to_block=to_block,
            argument_filters=_filters,
        )
        return block_filter

    @staticmethod
    def _method_mapper(method):
        if method == 'ENTITY':
            raise ValueError(f'Method {method} not implemented')
        if method == 'ACTIVITY':
            raise ValueError(f'Method {method} not implemented')
        if method == 'WAS_GENERATED_BY':
            return DIDRegistry.PROVENANCE_WAS_GENERATED_BY_EVENT_NAME
        if method == 'USED':
            return DIDRegistry.PROVENANCE_USED_EVENT_NAME
        if method == 'WAS_INFORMED_BY':
            raise ValueError(f'Method {method} not implemented')
        if method == 'WAS_STARTED_BY':
            raise ValueError(f'Method {method} not implemented')
        if method == 'WAS_ENDED_BY':
            raise ValueError(f'Method {method} not implemented')
        if method == 'WAS_INVALIDATED_BY':
            raise ValueError(f'Method {method} not implemented')
        if method == 'WAS_DERIVED_FROM':
            return DIDRegistry.PROVENANCE_WAS_DERIVED_FROM_EVENT_NAME
        if method == 'AGENT':
            raise ValueError(f'Method {method} not implemented')
        if method == 'WAS_ATTRIBUTED_TO':
            raise ValueError(f'Method {method} not implemented')
        if method == 'WAS_ASSOCIATED_WITH':
            return DIDRegistry.PROVENANCE_WAS_ASSOCIATED_WITH_EVENT_NAME
        if method == 'ACTED_ON_BEHALF':
            return DIDRegistry.PROVENANCE_ACTED_ON_BEHALF_EVENT_NAME
        else:
            raise ValueError(f'Method {method} is not implemented in the provenance specificacion.')
