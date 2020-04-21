#  Copyright 2018 Ocean Protocol Foundation
#  SPDX-License-Identifier: Apache-2.0

from contracts_lib_py.templates.template_manager import TemplateStoreManager
from tests.resources.tiers import e2e_test


@e2e_test
def test_template():
    template_store_manager = TemplateStoreManager('TemplateStoreManager')
    assert template_store_manager.get_num_templates() == 2
