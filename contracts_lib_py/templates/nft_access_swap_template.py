import logging

from contracts_lib_py.templates.template_base import TemplateBase

logger = logging.getLogger('AccessProofTemplate')


class NFTAccessSwapTemplate(TemplateBase):
    """Class representing the AccessProofTemplate contract."""
    CONTRACT_NAME = 'NFTAccessSwapTemplate'
