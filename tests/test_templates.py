from core.data_import import TemplateManager


def test_templates_list():
    t = TemplateManager()
    names = t.list_templates()
    assert isinstance(names, list)
