from contracts_lib_py.templates.template_manager import TemplateStoreManager


def test_template():
    template_store_manager = TemplateStoreManager('TemplateStoreManager')
    assert template_store_manager.get_num_templates() == 8
