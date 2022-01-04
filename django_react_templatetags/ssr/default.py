"""
This modules manages SSR rendering logic
"""

import json
import logging

import requests
from django.conf import settings

logger = logging.getLogger(__name__)


class SSRService:
    def load_or_empty(self, component, headers={}, ssr_context=None):
        request_json = (
            '{{"componentName": "{0}", "props": {1}, "context": {2}}}'.format(
                component["name"],
                component["json"],
                json.dumps(ssr_context) if ssr_context else {},
            )
        )

        try:
            inner_html = self.load(request_json, headers)
        except requests.exceptions.RequestException as e:
            inner_html = ""

            msg = "SSR request to '{}' failed: {}".format(
                settings.REACT_RENDER_HOST, e.__class__.__name__
            )
            logger.exception(msg)

        return {
            "html": inner_html,
            "params": {},
        }

    def load(self, request_json, headers):
        req = requests.post(
            settings.REACT_RENDER_HOST,
            timeout=get_request_timeout(),
            data=request_json,
            headers=headers,
        )

        req.raise_for_status()
        return req.text


def get_request_timeout():
    if not hasattr(settings, "REACT_RENDER_TIMEOUT"):
        return 20

    return settings.REACT_RENDER_TIMEOUT
