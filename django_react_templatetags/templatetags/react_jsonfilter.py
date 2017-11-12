# -*- coding: utf-8 -*-

"""
Simplified json encoder filter for react_django_templatetags.

Example:
    {{ my_dict|react_json }}
"""

from __future__ import unicode_literals
import json

from django import template
from django.utils.safestring import mark_safe

from django_react_templatetags.encoders import ReactRepresentationJSONEncoder


register = template.Library()


@register.filter('react_json')
def json_filter(value):
    return mark_safe(json.dumps(value, cls=ReactRepresentationJSONEncoder))
