# -*- coding: utf-8 -*-

"""
json encoder that also passes context for react_django_templatetags.

Example:
    {% react_render_json my_dict %}
"""

from __future__ import unicode_literals
import json

from django import template
from django.utils.safestring import mark_safe

from django_react_templatetags.encoders import json_encoder_cls_factory


register = template.Library()


@register.simple_tag(takes_context=True)
def react_render_json(context, value):
    cls = json_encoder_cls_factory(context)
    return mark_safe(json.dumps(value, cls=cls))
