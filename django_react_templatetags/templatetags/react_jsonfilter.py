# -*- coding: utf-8 -*-

"""
Simplified json encoder filter for react_django_templatetags.

Example:
    {{ my_dict|react_json }}
"""

from __future__ import unicode_literals
import json
import django
from django import template
from django.utils.safestring import mark_safe

if django.VERSION >= (1, 10):
    from django.core.serializers.json import DjangoJSONEncoder
else:
    from django_react_templatetags.serializers import DjangoJSONEncoder

register = template.Library()


@register.filter('react_json')
def json_filter(value):
    return mark_safe(json.dumps(value, cls=DjangoJSONEncoder))
