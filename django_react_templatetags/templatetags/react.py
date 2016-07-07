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

    def __init__(self, identifier, component, data=None):
        component_prefix = ""
        if hasattr(settings, "REACT_COMPONENT_PREFIX"):
            component_prefix = settings.REACT_COMPONENT_PREFIX

        self.identifier = identifier
        self.component = "%s%s" % (component_prefix, component)
        self.data = data

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
            identifier = "%s_%s" % (self.component, get_uuid())

        component = {
            "identifier": identifier,
            "component": self.component,
            "data": resolved_data,
        }

        components.append(component)
        context[CONTEXT_KEY] = components

        return u'<div id="%s"></div>' % identifier


def _prepare_args(parses, token):
    """
    Normalize token arguments that can be passed along to node renderer
    """

    values = {
        "identifier": None,
        "data": None
    }

    args = token.split_contents()
    method = args[0]

    for arg in args[1:]:
        key, value = arg.split(r'=',)

        if key == "id":
            key = "identifier"

        if value.startswith('"') or value.startswith('\''):
            value = value[1:-1]
        else:
            value = template.Variable(value)

        values[key] = value

    assert "component" in values, "%s is missing component value" % method

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
        "components": components
    }
