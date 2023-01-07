import logging
import re

import hypernova
from django.conf import settings

logger = logging.getLogger(__name__)
hypernova_id_re = re.compile(r"data-hypernova-id=\"([\w\-]*)\"")
hypernova_key_re = re.compile(r"data-hypernova-key=\"([\w\-]*)\"")


class HypernovaService:
    def load_or_empty(self, component, headers={}, ssr_context=None):
        # from hypernova.plugins.dev_mode import DevModePlugin

        renderer = hypernova.Renderer(
            settings.REACT_RENDER_HOST,
            # [DevModePlugin(logger)] if settings.DEBUG else [],
            [],
            timeout=get_request_timeout(),
            headers=headers,
        )

        inner_html = ""
        try:
            props = component["json_obj"]
            if ssr_context:
                props["context"] = ssr_context
            inner_html = renderer.render({component["name"]: props})
        except Exception as e:
            msg = "SSR request to '{}' failed: {}".format(
                settings.REACT_RENDER_HOST, e.__class__.__name__
            )
            logger.exception(msg)

        if not inner_html:
            return {"html": "", "params": {}}

        match = re.search(hypernova_id_re, inner_html)
        hypernova_id = match.group(1) if match else None

        match = re.search(hypernova_key_re, inner_html)
        hypernova_key = match.group(1) if match else None

        return {
            "html": inner_html,
            "params": {
                "hypernova_id": hypernova_id,
                "hypernova_key": hypernova_key,
            },
        }


def get_request_timeout():
    if not hasattr(settings, "REACT_RENDER_TIMEOUT"):
        return 20

    return settings.REACT_RENDER_TIMEOUT
