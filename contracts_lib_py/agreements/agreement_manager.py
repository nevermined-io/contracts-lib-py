from collections import namedtuple

from eth_utils import add_0x_prefix

from contracts_lib_py import ContractBase

AgreementValues = namedtuple(
    'AgreementValues',
    ('did', 'owner', 'template_id', 'condition_ids', 'condition_id_seeds', 'id_seed')
)


class AgreementStoreManager(ContractBase):
    """Class representing the AgreementStoreManager contract."""
    CONTRACT_NAME = 'AgreementStoreManager'

    def create_agreement(self, agreement_id, did, condition_types, condition_ids, time_locks,
                         time_outs):
        """
        Create a new agreement.
        The agreement will create conditions of conditionType with conditionId.
        Only "approved" templates can access this function.
        :param agreement_id:id of the agreement, hex str
        :param did: DID of the asset. The DID must be registered beforehand, bytes32
        :param condition_types: is a list of addresses that point to Condition contracts,
                                list(address)
        :param condition_ids: is a list of bytes32 content-addressed Condition IDs, bytes32
        :param time_locks: is a list of uint time lock values associated to each Condition, int
        :param time_outs: is a list of uint time out values associated to each Condition, int
        :return: bool
        """

        tx_hash = self.contract.caller.createAgreement(
            agreement_id,
            did,
            condition_types,
            condition_ids,
            time_locks,
            time_outs,
        )
        return self.is_tx_successful(tx_hash)

    def set_templates(self, temp):
        self.templates = temp

    def get_agreement(self, agreement_id):
        """
        Retrieve the agreement for a agreement_id.

        :param agreement_id: id of the agreement, hex str
        :return: the agreement attributes.
        """
        # get info from events
        template = self.contract.caller.getAgreementTemplate(agreement_id)
        event = self.templates[template].subscribe_agreement_created(
            agreement_id, 15, None, (), wait=True, from_block=0
        )
        agreement = event.args
        did = add_0x_prefix(agreement._did.hex())
        cond_ids = [add_0x_prefix(_id.hex()) for _id in agreement._conditionIds]
        cond_id_seeds = [add_0x_prefix(_id.hex()) for _id in agreement._conditionIdSeeds]

        return AgreementValues(
            did,
            agreement._creator,
            template,
            cond_ids,
            cond_id_seeds,
            agreement._idSeed
        )

    def get_agreement_did_owner(self, agreement_id):
        """Get the DID owner for this agreement with _id.

        :param agreement_id: id of the agreement, hex str
        :return: the DID owner associated with agreement.did from the DID registry.
        """
        return self.contract.caller.getAgreementDIDOwner(agreement_id)

    def get_num_agreements(self):
        """Return the size of the Agreements list.

        :return: the length of the agreement list, int
        """
        return self.contract.caller.getAgreementListSize()

    def hash_id(self, did_seed, address):
        """
        Calculates the final DID given a DID seed and the publisher address
        :param did_seed: the hash used to generate the did
        :param address: the address of the account creating the asset
        :return: the final DID
        """
        return add_0x_prefix(self.contract.caller.agreementId(did_seed, address).hex())
