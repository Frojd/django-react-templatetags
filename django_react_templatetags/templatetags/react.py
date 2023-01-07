"""
This module contains tags for including react components into templates.
"""
import json
import uuid

from django import template
from django.conf import settings
from django.template import Node
from django.utils.module_loading import import_string

from django_react_templatetags.encoders import json_encoder_cls_factory

register = template.Library()

CONTEXT_KEY = "REACT_COMPONENTS"

DEFAULT_SSR_HEADERS = {
    "Content-type": "application/json",
    "Accept": "text/plain",
}


def get_uuid():
    return uuid.uuid4().hex


def has_ssr(request):
    if request and request.META.get("HTTP_X_DISABLE_SSR"):
        return False

    return hasattr(settings, "REACT_RENDER_HOST") and settings.REACT_RENDER_HOST


def get_ssr_headers():
    if not hasattr(settings, "REACT_RENDER_HEADERS"):
        return DEFAULT_SSR_HEADERS
    return settings.REACT_RENDER_HEADERS


def load_from_ssr(component, ssr_context=None):
    ssr_service = _get_ssr_service()()
    return ssr_service.load_or_empty(
        component,
        headers=get_ssr_headers(),
        ssr_context=ssr_context,
    )


def _get_ssr_service():
    """
    Loads a custom React Tag Manager if provided in Django Settings.
    """

    class_path = getattr(settings, "REACT_SSR_SERVICE", "")
    if not class_path:
        from django_react_templatetags.ssr.default import SSRService

        return SSRService

    return import_string(class_path)


class ReactTagManager(Node):
    """
    Handles the printing of react placeholders and queueing, is invoked by
    react_render.
    """

    def __init__(
        self,
        identifier,
        component,
        data=None,
        css_class=None,
        props=None,
        ssr_context=None,
        no_placeholder=None,
    ):
        component_prefix = ""
        if hasattr(settings, "REACT_COMPONENT_PREFIX"):
            component_prefix = settings.REACT_COMPONENT_PREFIX

        self.identifier = identifier
        self.component = component
        self.component_prefix = component_prefix
        self.data = data
        self.css_class = css_class
        self.props = props
        self.ssr_context = ssr_context
        self.no_placeholder = no_placeholder

    def render(self, context):
        qualified_component_name = self.get_qualified_name(context)
        identifier = self.get_identifier(context, qualified_component_name)
        component_props = self.get_component_props(context)
        json_str = self.props_to_json(component_props, context)

        component = {
            "identifier": identifier,
            "data_identifier": "{}_data".format(identifier),
            "name": qualified_component_name,
            "json": json_str,
            "json_obj": json.loads(json_str),
        }

        placeholder_attr = (
            ("id", identifier),
            ("class", self.resolve_template_variable(self.css_class, context)),
        )
        placeholder_attr = [x for x in placeholder_attr if x[1] is not None]

        component_html = ""
        if has_ssr(context.get("request", None)):
            ssr_resp = load_from_ssr(
                component,
                ssr_context=self.get_ssr_context(context),
            )
            component_html = ssr_resp["html"]
            component["ssr_params"] = ssr_resp["params"]

        components = context.get(CONTEXT_KEY, [])
        components.append(component)
        context[CONTEXT_KEY] = components

        if self.no_placeholder:
            return component_html

        return self.render_placeholder(placeholder_attr, component_html)

    def get_qualified_name(self, context):
        component_name = self.resolve_template_variable(self.component, context)
        return "{}{}".format(self.component_prefix, component_name)

    def get_identifier(self, context, qualified_component_name):
        identifier = self.resolve_template_variable(self.identifier, context)

        if identifier:
            return identifier

        return "{}_{}".format(qualified_component_name, get_uuid())

    def get_component_props(self, context):
        resolved_data = self.resolve_template_variable_else_none(self.data, context)
        resolved_data = resolved_data if resolved_data else {}

        for prop in self.props:
            data = self.resolve_template_variable_else_none(
                self.props[prop],
                context,
            )
            resolved_data[prop] = data

        return resolved_data

    def get_ssr_context(self, context):
        if not self.ssr_context:
            return {}

        return self.resolve_template_variable(self.ssr_context, context)

    @staticmethod
    def resolve_template_variable(value, context):
        if isinstance(value, template.Variable):
            return value.resolve(context)

        return value

    @staticmethod
    def resolve_template_variable_else_none(value, context):
        try:
            data = value.resolve(context)
        except template.VariableDoesNotExist:
            data = None
        except AttributeError:
            data = None

        return data

    @staticmethod
    def props_to_json(resolved_data, context):
        cls = json_encoder_cls_factory(context)
        return json.dumps(resolved_data, cls=cls)

    @staticmethod
    def render_placeholder(attributes, component_html=""):
        attr_pairs = map(lambda x: '{}="{}"'.format(*x), attributes)
        return "<div {}>{}</div>".format(
            " ".join(attr_pairs),
            component_html,
        )


@register.tag
def react_render(parser, token):
    """
    Renders a react placeholder and adds it to the global render queue.

    Example:
        {% react_render component="ListRestaurants" data=restaurants %}
    """

    values = _prepare_args(parser, token)
    tag_manager = _get_tag_manager()
    return tag_manager(**values)


def _prepare_args(parses, token):
    """
    Normalize token arguments that can be passed along to node renderer
    """

    values = {
        "identifier": None,
        "css_class": None,
        "data": None,
        "props": {},
    }

    key_mapping = {
        "id": "identifier",
        "class": "css_class",
        "props": "data",
    }

    args = token.split_contents()
    method = args[0]

    for arg in args[1:]:
        key, value = arg.split(
            r"=",
        )

        key = key_mapping.get(key, key)
        is_standalone_prop = key.startswith("prop_")
        if is_standalone_prop:
            key = key[5:]

        value = template.Variable(value)
        if is_standalone_prop:
            values["props"][key] = value
        else:
            values[key] = value

    assert "component" in values, "{} is missing component value".format(method)  # NOQA

    return values


def _get_tag_manager():
    """
    Loads a custom React Tag Manager if provided in Django Settings.
    """

    class_path = getattr(settings, "REACT_RENDER_TAG_MANAGER", "")
    if not class_path:
        return ReactTagManager

    return import_string(class_path)


@register.inclusion_tag("react_print.html", takes_context=True)
def react_print(context):
    """
    Generates ReactDOM.hydate calls based on REACT_COMPONENT queue,
    this needs to be run after react has been loaded.

    The queue will be cleared after beeing called.

    Example:
        {% react_print %}
    """
    components = context.get(CONTEXT_KEY, [])
    context[CONTEXT_KEY] = []

    new_context = context.__copy__()
    new_context["ssr_available"] = has_ssr(context.get("request", None))
    new_context["components"] = components

    return new_context
