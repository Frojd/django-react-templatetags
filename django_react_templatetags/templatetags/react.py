# -*- coding: utf-8 -*-

"""
This module contains tags for including react components into templates.
"""
import uuid

from django import template
from django.conf import settings
from django.template import Node


register = template.Library()

CONTEXT_KEY = "REACT_COMPONENTS"
CONTEXT_PROCESSOR = 'django_react_templatetags.context_processors.react_context_processor'  # NOQA


def get_uuid():
    return uuid.uuid4().hex


class ReactTagManager(Node):
    """
    Handles the printing of react placeholders and queueing, is invoked by
    react_render.
    """

    def __init__(self, identifier, component, data=None, css_class=None):
        component_prefix = ""
        if hasattr(settings, "REACT_COMPONENT_PREFIX"):
            component_prefix = settings.REACT_COMPONENT_PREFIX

        self.identifier = identifier
        self.component = component
        self.component_prefix = component_prefix
        self.data = data
        self.css_class = css_class

    def _has_processor(self):
        try:
            status = CONTEXT_PROCESSOR in settings.TEMPLATES[0]['OPTIONS']['context_processors']  # NOQA
        except Exception as e:  # NOQA
            status = False

        return status

    def render(self, context):
        if not self._has_processor():
            raise Exception('"react_context_processor must be added to TEMPLATE_CONTEXT_PROCESSORS"')  # NOQA

        components = context.get(CONTEXT_KEY, [])

        component_name = self.component
        if isinstance(self.component, template.Variable):
            component_name = self.component.resolve(context)

        component = "{}{}".format(self.component_prefix, component_name)

        try:
            resolved_data = self.data.resolve(context)
        except template.VariableDoesNotExist:
            resolved_data = None
        except AttributeError:
            resolved_data = None

        identifier = self.identifier
        if isinstance(self.identifier, template.Variable):
            identifier = self.identifier.resolve(context)
        elif not identifier:
            identifier = "{}_{}".format(component, get_uuid())

        component = {
            "identifier": identifier,
            "component": component,
            "data": resolved_data,
        }

        components.append(component)
        context[CONTEXT_KEY] = components

        div_attr = (
            ("id", identifier),
            ("class", self.css_class),
        )
        div_attr = [x for x in div_attr if x[1] is not None]
        attr_pairs = map(lambda x: '{}="{}"'.format(*x), div_attr)

        return u'<div {}></div>'.format(" ".join(attr_pairs))


def _prepare_args(parses, token):
    """
    Normalize token arguments that can be passed along to node renderer
    """

    values = {
        "identifier": None,
        "css_class": None,
        "data": None
    }

    args = token.split_contents()
    method = args[0]

    for arg in args[1:]:
        key, value = arg.split(r'=',)

        if key == "id":
            key = "identifier"

        if key == "class":
            key = "css_class"

        if value.startswith('"') or value.startswith('\''):
            value = value[1:-1]
        else:
            value = template.Variable(value)

        values[key] = value

    assert "component" in values, "{} is missing component value".format(method)  # NOQA

    return values


@register.tag
def react_render(parser, token):
    """
    Renders a react placeholder and adds it to the global render queue.

    Example:
        {% react_render component="ListRestaurants" data=restaurants %}
    """

    values = _prepare_args(parser, token)
    return ReactTagManager(**values)


@register.inclusion_tag('react_print.html', takes_context=True)
def react_print(context):
    """
    Generates ReactDOM.render calls based on REACT_COMPONENT queue,
    this needs to be run after react has been loaded.

    The queue will be cleared after beeing called.

    Example:
        {% react_print %}
    """
    components = context[CONTEXT_KEY]
    context[CONTEXT_KEY] = []

    return {
        "components": components,
    }
