# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django

from django_react_templatetags.mixins import RepresentationMixin

if django.VERSION >= (1, 10):
    from django.core.serializers.json import DjangoJSONEncoder
else:
    from django_react_templatetags.serializers import DjangoJSONEncoder


class ReactRepresentationJSONEncoder(DjangoJSONEncoder):
    '''
    Custom json encoder that adds support for RepresentationMixin
    '''
    def default(self, o):
        if isinstance(o, RepresentationMixin):
            return o.react_representation
        return super(ReactRepresentationJSONEncoder, self).default(o)
