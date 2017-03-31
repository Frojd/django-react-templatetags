from django.conf import global_settings
from django.template import Context, Template
from django.test import TestCase, modify_settings, override_settings
from tests.models import Person


@modify_settings(INSTALLED_APPS={'append': 'django_react_templatetags'})
@override_settings(
    MIDDLEWARE_CLASSES=global_settings.MIDDLEWARE_CLASSES,
    TEMPLATES=[{
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': True,
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.core.context_processors.debug',
                'django.core.context_processors.i18n',
                'django.core.context_processors.media',
                'django.core.context_processors.static',
                'django.core.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'django.core.context_processors.request',

                # Project specific
                'django_react_templatetags.context_processors.react_context_processor',  # NOQA
            ],
        },
    }],
    SITE_ID=1,
)
class ReactIncludeComponentTest(TestCase):
    def setUp(self):
        self.mocked_context = Context({'REACT_COMPONENTS': []})

    def test_react_tag(self):
        "The react_render inserts one components into the template"

        out = Template(
            "{% load react %}"
            "{% react_render component=\"Component\" %}"
        ).render(self.mocked_context)

        self.assertTrue('<div id="Component_' in out)

    def test_multiple_tags(self):
        "The react_render inserts two components into the template"

        out = Template(
            "{% load react %}"
            "{% react_render component=\"Component\" %}"
            "{% react_render component=\"Component\" %}"
        ).render(self.mocked_context)

        self.assertTrue('<div id="Component_' in out)
        self.assertEquals(len(self.mocked_context.get("REACT_COMPONENTS")), 2)

    def test_component_name_from_variable(self):
        "The react_render inserts with a component id as a variable"

        self.mocked_context["component_name"] = 'DynamicComponentName'

        out = Template(
            "{% load react %}"
            "{% react_render component=component_name %}"
            "{% react_print %}"
        ).render(self.mocked_context)

        self.assertTrue('React.createElement(DynamicComponentName' in out)

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

        self.assertTrue('<div id="Components.Component_' in out)

    def test_print_tag(self):
        "Makes sure the react_render gets emptied from context after print"

        out = Template(
            "{% load react %}"
            "{% react_render component=\"Component\" %}"
            "{% react_print %}"
        ).render(self.mocked_context)

        self.assertTrue('ReactDOM.render(' in out)
        self.assertTrue('React.createElement(Component' in out)
        self.assertEquals(len(self.mocked_context.get("REACT_COMPONENTS")), 0)

    @override_settings(
        REACT_COMPONENT_PREFIX="ReactNamespace."
    )
    def test_print_tag_prefix(self):
        "Makes sure react_print outputs ReactDOM.render with react prefix"

        out = Template(
            "{% load react %}"
            "{% react_render component=\"Component\" %}"
            "{% react_print %}"
        ).render(self.mocked_context)

        self.assertTrue('React.createElement(ReactNamespace.Component' in out)

    def test_variable_identifier(self):
        "Tests that the identifier variable is evaluated as variable"

        self.mocked_context["component_identifier"] = "TomWaits"

        out = Template(
            "{% load react %}"
            "{% react_render component=\"Component\" identifier=component_identifier %}"  # NOQA
            "{% react_print %}"
        ).render(self.mocked_context)

        self.assertTrue('TomWaits' in out)

    def test_class_property(self):
        "Makes sure class property are applied"

        out = Template(
            "{% load react %}"
            "{% react_render component=\"Component\" class=\"component-class\" %}"  # NOQA
        ).render(self.mocked_context)

        self.assertTrue('class="component-class"' in out)

    def test_model_representation_data(self):
        "Tests that react representation of model is transformed"

        person = Person(first_name='Tom', last_name='Waits')

        self.mocked_context["component_data"] = person

        out = Template(
            "{% load react %}"
            "{% react_render component=\"Component\" data=component_data %}"
            "{% react_print %}"
        ).render(self.mocked_context)

        self.assertTrue('{"first_name": "Tom", "last_name": "Waits"}' in out)
