import logging
import json

from django.conf import settings
import hypernova


logger = logging.getLogger(__name__)


class HypernovaService():
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
            props = json.loads(component['json'])
            if ssr_context:
                props['context'] = ssr_context
            inner_html = renderer.render({component['name']: props})
        except Exception as e:
            msg = "SSR request to '{}' failed: {}".format(
                settings.REACT_RENDER_HOST,
                e.__class__.__name__
            )
            logger.exception(msg)

        return inner_html


def get_request_timeout():
    if not hasattr(settings, 'REACT_RENDER_TIMEOUT'):
        return 20

    return settings.REACT_RENDER_TIMEOUT
