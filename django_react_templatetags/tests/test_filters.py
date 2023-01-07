import re

import django
from django.template import Context, Template
from django.test import SimpleTestCase, override_settings
from django.test.client import RequestFactory

from django_react_templatetags.tests.demosite.models import Movie, Person


class ReactIncludeComponentTest(SimpleTestCase):
    def setUp(self):
        self.mocked_context = Context({"REACT_COMPONENTS": []})

    def test_react_tag(self):
        "The react_render inserts one components into the template"

        out = Template(
            "{% load react %}" '{% react_render component="Component" %}'
        ).render(self.mocked_context)

        self.assertTrue('<div id="Component_' in out)

    def test_multiple_tags(self):
        "The react_render inserts two components into the template"

        out = Template(
            "{% load react %}"
            '{% react_render component="Component" %}'
            '{% react_render component="Component" %}'
        ).render(self.mocked_context)

        self.assertTrue('<div id="Component_' in out)
        self.assertEquals(len(self.mocked_context.get("REACT_COMPONENTS")), 2)

    def test_component_name_from_variable(self):
        "The react_render inserts with a component id as a variable"

        self.mocked_context["component_name"] = "DynamicComponentName"

        out = Template(
            "{% load react %}"
            "{% react_render component=component_name %}"
            "{% react_print %}"
        ).render(self.mocked_context)

        self.assertTrue("React.createElement(DynamicComponentName" in out)

    def test_react_json_data_tag(self):
        "Tests that the data is added as correct json into the react render"

        self.mocked_context["component_data"] = {"name": "Tom Waits"}

        out = Template(
            "{% load react %}"
            '{% react_render component="Component" data=component_data %}'
            "{% react_print %}"
        ).render(self.mocked_context)

        self.assertTrue('{"name": "Tom Waits"}' in out)

    @override_settings(REACT_COMPONENT_PREFIX="Components.")
    def test_react_component_prefix(self):
        "Tests that a prefix is added to the component createElement script"

        out = Template(
            "{% load react %}" '{% react_render component="Component" %}'
        ).render(self.mocked_context)

        self.assertTrue('<div id="Components.Component_' in out)

    def test_print_tag(self):
        "Makes sure the react_render gets emptied from context after print"

        out = Template(
            "{% load react %}"
            '{% react_render component="Component" %}'
            "{% react_print %}"
        ).render(self.mocked_context)

        self.assertTrue("ReactDOM.render(" in out)
        self.assertTrue("React.createElement(Component" in out)
        self.assertEquals(len(self.mocked_context.get("REACT_COMPONENTS")), 0)

    @override_settings(REACT_COMPONENT_PREFIX="ReactNamespace.")
    def test_print_tag_prefix(self):
        "Makes sure react_print outputs ReactDOM.render with react prefix"

        out = Template(
            "{% load react %}"
            '{% react_render component="Component" %}'
            "{% react_print %}"
        ).render(self.mocked_context)

        self.assertTrue("React.createElement(ReactNamespace.Component" in out)

    def test_variable_identifier(self):
        "Tests that the identifier variable is evaluated as variable"

        self.mocked_context["component_identifier"] = "TomWaits"

        out = Template(
            "{% load react %}"
            '{% react_render component="Component" identifier=component_identifier %}'  # NOQA
            "{% react_print %}"
        ).render(self.mocked_context)

        self.assertTrue("TomWaits" in out)

    def test_class_property(self):
        "Makes sure class property are applied"

        out = Template(
            "{% load react %}"
            '{% react_render component="Component" class="component-class" %}'  # NOQA
        ).render(self.mocked_context)

        self.assertTrue('class="component-class"' in out)

    def test_unresolved_props_wont_raise_error(self):
        "Makes sure class property are applied"

        out = Template(
            "{% load react %}"
            '{% react_render component="Component" props=nonexisting_val %}'  # NOQA
        ).render(self.mocked_context)

        self.assertTrue('<div id="' in out)

    def test_class_property_from_variable(self):
        self.mocked_context["class_name"] = "component-class"

        out = Template(
            "{% load react %}"
            '{% react_render component="Component" class=class_name %}'  # NOQA
        ).render(self.mocked_context)

        self.assertTrue('class="component-class"' in out)

    def test_model_representation_data(self):
        "Tests that react representation of model is transformed"

        person = Person(first_name="Tom", last_name="Waits")

        self.mocked_context["component_data"] = person

        out = Template(
            "{% load react %}"
            '{% react_render component="Component" data=component_data %}'
            "{% react_print %}"
        ).render(self.mocked_context)

        self.assertTrue('"first_name": "Tom"' in out)
        self.assertTrue('"last_name": "Waits"' in out)

    def test_no_represntation_mixin_raises_error(self):
        if django.VERSION < (3, 0):
            "Skip this test in django 2 due to different output format"
            return

        class NoRepresentation(object):
            pass

        instance = NoRepresentation()
        self.mocked_context["component_data"] = instance

        with self.assertRaises(TypeError) as err:
            out = Template(
                "{% load react %}"
                '{% react_render component="Component" data=component_data %}'
                "{% react_print %}"
            ).render(self.mocked_context)

        self.assertTrue(
            re.search(
                r"Object of type \'{,1}NoRepresentation\'{,1} is not JSON serializable",
                str(err.exception),
            )
        )

    def test_individual_prop_data(self):
        "Tests that templatetag can accept individual prop types"

        person = Person(first_name="Tom", last_name="Waits")

        self.mocked_context["person"] = person
        self.mocked_context["album"] = "Small Change"

        out = Template(
            "{% load react %}"
            '{% react_render component="Component" prop_person=person prop_album=album %}'  # NOQA
            "{% react_print %}"
        ).render(self.mocked_context)

        self.assertTrue('person":' in out)
        self.assertFalse('prop_person":' in out)
        self.assertTrue('"first_name": "Tom"' in out)
        self.assertTrue('"last_name": "Waits"' in out)
        self.assertTrue('album": "Small Change"' in out)

    def test_combined_data_and_individual_props(self):
        "Tests that templatetag can accept individual prop types"

        person = Person(first_name="Tom", last_name="Waits")

        self.mocked_context["person"] = person
        self.mocked_context["component_data"] = {"name": "Tom Waits"}

        out = Template(
            "{% load react %}"
            '{% react_render component="Component" data=component_data prop_person=person %}'  # NOQA
            "{% react_print %}"
        ).render(self.mocked_context)

        self.assertTrue('person":' in out)
        self.assertTrue('"first_name": "Tom"' in out)
        self.assertTrue('"last_name": "Waits"' in out)
        self.assertTrue('name": "Tom Waits"' in out)

    def test_support_for_props_data_fallback_arg(self):
        "Tests that templatetag can accept individual prop types"

        self.mocked_context["component_data"] = {"name": "Tom Waits"}

        out = Template(
            "{% load react %}"
            '{% react_render component="Component" props=component_data %}'  # NOQA
            "{% react_print %}"
        ).render(self.mocked_context)

        self.assertTrue('"name": "Tom Waits"' in out)

    def test_to_model_representation_data(self):
        "Tests that to_react_representation renders proper json"

        movie = Movie(title="Night On Earth", year=1991)

        self.mocked_context["component_data"] = movie
        self.mocked_context["request"] = RequestFactory().get("/random")

        out = Template(
            "{% load react %}"
            '{% react_render component="Component" data=component_data %}'
            "{% react_print %}"
        ).render(self.mocked_context)

        self.assertTrue('"title": "Night On Earth"' in out)
        self.assertTrue('"year": 1991' in out)
        self.assertTrue('"current_path": "/random"' in out)

    def test_unicode_chars(self):
        "Tests that the data is added as correct json into the react render"

        self.mocked_context["component_data"] = {"name": "ÅÄÖ"}

        out = Template(
            "{% load react %}"
            '{% react_render component="Component" data=component_data %}'
            "{% react_print %}"
        ).render(self.mocked_context)

        self.assertTrue('{"name": "\\u00c5\\u00c4\\u00d6"}' in out)

    def test_prop_strings_not_null(self):
        "Test that standalone string props are not returned as null"

        out = Template(
            "{% load react %}"
            '{% react_render component="Component" prop_country="Sweden" %}'
            "{% react_print %}"
        ).render(self.mocked_context)

        self.assertTrue('{"country": "Sweden"}' in out)

    def test_no_placeholder_returns_nothing(self):
        out = Template(
            "{% load react %}"
            '{% react_render component="Component" prop_country="Sweden" no_placeholder=1 %}'
            "{% react_print %}"
        ).render(self.mocked_context)

        self.assertFalse(out.startswith('<div id="Component_'))
        self.assertTrue('{"country": "Sweden"}' in out)

    def test_data_script_is_included(self):
        out = Template(
            "{% load react %}"
            '{% react_render component="Component" identifier="my_id" %}'
            "{% react_print %}"
        ).render(self.mocked_context)

        self.assertFalse(
            out.startswith('<script id="my_id_data" type="application/json"')
        )
