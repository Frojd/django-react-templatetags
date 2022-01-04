try:
    from unittest import mock
except ImportError:
    import mock

from django.test import SimpleTestCase, override_settings
from django.urls import reverse


@override_settings(
    REACT_RENDER_HOST="http://react-service.dev/",
    REACT_SSR_SERVICE="django_react_templatetags.tests.test_ssr_custom_service.CustomSSRService",
)
class CustomSSRServiceTest(SimpleTestCase):
    @mock.patch(
        "django_react_templatetags.tests.test_ssr_custom_service.CustomSSRService.load_or_empty"
    )
    def test_that_disable_ssr_header_disables_ssr(self, mocked_func):
        self.client.get(
            reverse("static_react_view"),
        )
        self.assertEqual(mocked_func.call_count, 1)


class CustomSSRService:
    "Used for testing using a custom ssr service"

    def load_or_empty(self, component, headers={}, ssr_context=None):
        pass
