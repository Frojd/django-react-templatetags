# -*- coding: utf-8 -*-

"""
This modules manages SSR rendering logic
"""
import logging

from django.conf import settings

import requests


logger = logging.getLogger(__name__)


def load_or_empty(self, component, props):
    inner_html = ''

    try:
        inner_html = load(component, props)
    except requests.exceptions.RequestException as e:
        logger.error(e)

    return inner_html


def load(self, component, props):
    req = requests.post(settings.REACT_RENDER_HOST, json={
        'componentName': component,
        'props': props
    })

    req.raise_for_status()
    return req.text
