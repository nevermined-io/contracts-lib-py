import logging

from contracts_lib_py.templates.template_base import TemplateBase

logger = logging.getLogger('AccessTemplate')


class AccessTemplate(TemplateBase):
    """Class representing the AccessTemplate contract."""
    CONTRACT_NAME = 'AccessTemplate'
