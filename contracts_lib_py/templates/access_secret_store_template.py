import logging

from contracts_lib_py.templates.template_base import TemplateBase

logger = logging.getLogger('escrowAccessSecretStoreTemplate')


class EscrowAccessSecretStoreTemplate(TemplateBase):
    """Class representing the EscrowAccessSecretStoreTemplate contract."""
    CONTRACT_NAME = 'EscrowAccessSecretStoreTemplate'
