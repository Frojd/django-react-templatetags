from django.conf import global_settings
from django.template import Context, Template
from django.test import TestCase, modify_settings, override_settings


@modify_settings(INSTALLED_APPS={'append': 'django_react_filters'})
@override_settings(
    MIDDLEWARE_CLASSES=global_settings.MIDDLEWARE_CLASSES,
    TEMPLATES=[],
    SITE_ID=1
)
class ReactIncludeComponentTest(TestCase):
    def setUp(self):
        self.mocked_context = Context({'REACT_COMPONENTS': []})

    def test_react_tag(self):
        "The react_rendered inserts two components into the template"

        out = Template(
            "{% load react %}"
            "{% react_render component=\"Component\" %}"
        ).render(self.mocked_context)

        self.assertTrue('<div id="Component_1"></div>' in out)

    def test_multiple_tags(self):
        "The react_rendered inserts two components into the template"

        out = Template(
            "{% load react %}"
            "{% react_render component=\"Component\" %}"
            "{% react_render component=\"Component\" %}"
        ).render(self.mocked_context)

        self.assertTrue('<div id="Component_2"></div>' in out)
        self.assertEquals(len(self.mocked_context.get("REACT_COMPONENTS")), 2)

    def test_react_json_data_tag(self):
        "Tests that the data is added as correct json into the react render"

        self.mocked_context["component_data"] = {'name': 'Tom Waits'}

        out = Template(
            "{% load react %}"
            "{% react_render component=\"Component\" data=component_data %}"
            "{% react_print %}"
        ).render(self.mocked_context)

        self.assertTrue('{"name": "Tom Waits"}' in out)

    @override_settings(
        REACT_COMPONENT_PREFIX="Components."
    )
    def test_react_component_prefix(self):
        "Tests that a prefix is added to the component createElement script"

        out = Template(
            "{% load react %}"
            "{% react_render component=\"Component\" %}"
        ).render(self.mocked_context)

        self.assertTrue('<div id="Components.Component_1"></div>' in out)

    def test_print_tag(self):
        "The react_rendered inserts two components into the template"

        out = Template(
            "{% load react %}"
            "{% react_render component=\"Component\" %}"
            "{% react_print %}"
        ).render(self.mocked_context)

        self.assertTrue('ReactDOM.render(' in out)
        self.assertTrue('React.createElement(Component' in out)
