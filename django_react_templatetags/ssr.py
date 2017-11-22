# -*- coding: utf-8 -*-

"""
This modules manages SSR rendering logic
"""

import logging
import json

from django.conf import settings
import requests

from django_react_templatetags.encoders import json_encoder_cls_factory


logger = logging.getLogger(__name__)


def load_or_empty(component, props, context):
    inner_html = ''

    try:
        inner_html = load(component, props, context)
    except requests.exceptions.RequestException as e:
        logger.error(e)

    return inner_html


def load(component, props, context):
    req_data = {
        'componentName': component,
        'props': props
    }
    cls = json_encoder_cls_factory(context)

    req = requests.post(
        settings.REACT_RENDER_HOST,
        timeout=get_request_timeout(),
        data=json.dumps(req_data, cls=cls)
    )

    req.raise_for_status()
    return req.text


def get_request_timeout():
    if not hasattr(settings, "REACT_RENDER_TIMEOUT"):
        return 20

    return settings.REACT_RENDER_TIMEOUT
