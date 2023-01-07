from django.template import Context, Template
from django.test import SimpleTestCase, override_settings

from django_react_templatetags.templatetags.react import (
    ReactTagManager,
    _get_tag_manager,
)


class TestReactTagManager(ReactTagManager):
    def render(self, context):
        return "Test"


class ReactIncludeComponentTest(SimpleTestCase):
    def setUp(self):
        self.mocked_context = Context({"REACT_COMPONENTS": []})

    def test_tag_manager_not_overridden(self):
        "Test that the default ReactTagManager is used by default"
        self.assertEqual(_get_tag_manager(), ReactTagManager)

    @override_settings(
        REACT_RENDER_TAG_MANAGER="django_react_templatetags.tests.test_manager.TestReactTagManager"
    )
    def test_tag_manager_overridden(self):
        "Test that the TestReactTagManager is actually used"
        self.assertEqual(_get_tag_manager(), TestReactTagManager)

        out = Template(
            "{% load react %}" '{% react_render component="Component" %}'
        ).render(self.mocked_context)

        self.assertEqual("Test", out)
