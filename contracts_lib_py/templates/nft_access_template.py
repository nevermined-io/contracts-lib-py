import logging

from contracts_lib_py.templates.template_base import TemplateBase

logger = logging.getLogger('nftAccessTemplate')


class NFTAccessTemplate(TemplateBase):
    """Class representing the NFTAccessTemplate contract."""
    CONTRACT_NAME = 'NFTAccessTemplate'
