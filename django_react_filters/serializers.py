# Avoid shadowing the standard library json module
from __future__ import absolute_import, unicode_literals

import datetime
import decimal
import json
import uuid

from django.utils import six
from django.utils.functional import Promise
from django.utils.timezone import is_aware


class DjangoJSONEncoder(json.JSONEncoder):
    """
    Future version of the built in encoder that supports proxy objects.
    https://code.djangoproject.com/ticket/25468

    Will be merged in Django 1.10
    """

    def default(self, o):
        # See "Date Time String Format" in the ECMA-262 specification.
        if isinstance(o, datetime.datetime):
            r = o.isoformat()
            if o.microsecond:
                r = r[:23] + r[26:]
            if r.endswith('+00:00'):
                r = r[:-6] + 'Z'
            return r
        elif isinstance(o, datetime.date):
            return o.isoformat()
        elif isinstance(o, datetime.time):
            if is_aware(o):
                raise ValueError("JSON can't represent timezone-aware times.")
            r = o.isoformat()
            if o.microsecond:
                r = r[:12]
            return r
        elif isinstance(o, decimal.Decimal):
            return str(o)
        elif isinstance(o, uuid.UUID):
            return str(o)
        elif isinstance(o, Promise):
            return six.text_type(o)
        else:
            return super(DjangoJSONEncoder, self).default(o)
