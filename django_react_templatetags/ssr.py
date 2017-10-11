# -*- coding: utf-8 -*-

"""
This modules manages SSR rendering logic
"""
import logging
import json

from django.conf import settings
import requests

from django_react_templatetags.encoders import ReactRepresentationJSONEncoder


logger = logging.getLogger(__name__)


def load_or_empty(component, props):
    inner_html = ''

    try:
        inner_html = load(component, props)
    except requests.exceptions.RequestException as e:
        logger.error(e)

    return inner_html


def load(component, props):
    req_data = {
        'componentName': component,
        'props': props
    }

    req = requests.post(settings.REACT_RENDER_HOST,
        timeout=get_request_timeout(),
        data=json.dumps(
        req_data, cls=ReactRepresentationJSONEncoder
    ))

    req.raise_for_status()
    return req.text


def get_request_timeout():
    if not hasattr(settings, "REACT_RENDER_TIMEOUT"):
        return 20

    return settings.REACT_RENDER_TIMEOUT

