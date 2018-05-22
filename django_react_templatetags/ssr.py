# -*- coding: utf-8 -*-

"""
This modules manages SSR rendering logic
"""

import logging
import json

from django.conf import settings
import requests


logger = logging.getLogger(__name__)


def load_or_empty(component, headers={}):
    request_json = u'{{"componentName": "{0}", "props": {1}}}'.format(
        component['name'],
        component['json'],
    )

    try:
        inner_html = load(request_json, headers)
    except requests.exceptions.RequestException as e:
        inner_html = ''
        logger.error(e)

    return inner_html


def load(request_json, headers):
    req = requests.post(
        settings.REACT_RENDER_HOST,
        timeout=get_request_timeout(),
        data=request_json,
        headers=headers,
    )

    req.raise_for_status()
    return req.text


def get_request_timeout():
    if not hasattr(settings, 'REACT_RENDER_TIMEOUT'):
        return 20

    return settings.REACT_RENDER_TIMEOUT
