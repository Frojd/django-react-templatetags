import json

try:
    from unittest import mock
except ImportError:
    import mock

from django.template import Context, Template
from django.test import SimpleTestCase, override_settings
from django.urls import reverse

from django_react_templatetags.ssr.default import SSRService
from django_react_templatetags.tests.demosite.models import MovieWithContext, Person

from .mock_response import MockResponse


@override_settings(
    REACT_RENDER_HOST="http://react-service.dev/",
)
class SSRTemplateTest(SimpleTestCase):
    def setUp(self):
        self.mocked_context = Context({"REACT_COMPONENTS": []})

    @mock.patch("requests.post")
    def test_verify_404(self, mocked):
        "The SSR rendering falls back to client side rendering if 404"

        mocked.side_effect = [MockResponse({"error": "not found"}, 404)]

        out = Template(
            "{% load react %}" '{% react_render component="Component" %}'
        ).render(self.mocked_context)

        self.assertTrue('<div id="Component_' in out)

    @mock.patch("requests.post")
    def test_that_only_html_resp_are_shown_in_template(self, mocked):
        mocked.side_effect = [MockResponse("<h1>Title</h1>", 200)]

        out = Template(
            "{% load react %}" '{% react_render component="Component" %}'
        ).render(self.mocked_context)

        self.assertFalse("{'html': " in out)

    @mock.patch("requests.post")
    def test_verify_rendition(self, mocked):
        "The SSR returns inner html"

        mocked.side_effect = [MockResponse("<h1>Title</h1>", 200)]

        out = Template(
            "{% load react %}" '{% react_render component="Component" %}'
        ).render(self.mocked_context)

        self.assertTrue("<h1>Title</h1>" in out)

    @mock.patch("requests.post")
    def test_request_body(self, mocked):
        "The SSR request sends the props in a expected way"

        mocked.side_effect = [MockResponse("<h1>Title</h1>", 200)]

        person = Person(first_name="Tom", last_name="Waits")

        self.mocked_context["person"] = person
        self.mocked_context["component_data"] = {"album": "Real gone"}

        Template(
            "{% load react %}"
            '{% react_render component="Component" prop_person=person data=component_data %}'  # NOQA
        ).render(self.mocked_context)

        request_body = {
            "componentName": "Component",
            "props": {
                "album": "Real gone",
                "person": {"first_name": "Tom", "last_name": "Waits"},
            },
            "context": {},
        }

        self.assertEqual(json.loads(mocked.call_args[1]["data"]), request_body)

    @mock.patch("requests.post")
    def test_request_body_context(self, mocked):
        "The SSR request sends the props in a expected way with context"

        mocked.side_effect = [MockResponse("<h1>Title</h1>", 200)]

        movie = MovieWithContext(title="Office space", year=1991)

        self.mocked_context["movie"] = movie
        self.mocked_context["search_term"] = "Stapler"

        Template(
            "{% load react %}"
            '{% react_render component="Component" prop_movie=movie %}'
        ).render(self.mocked_context)

        request_body = {
            "componentName": "Component",
            "props": {
                "movie": {
                    "title": "Office space",
                    "year": 1991,
                    "search_term": "Stapler",
                }
            },
            "context": {},
        }

        self.assertEqual(json.loads(mocked.call_args[1]["data"]), request_body)

    @mock.patch("requests.post")
    def test_request_body_with_ssr_context(self, mocked):
        "The SSR request appends the 'ssr_context' in an expected way"

        mocked.side_effect = [MockResponse("<h1>Title</h1>", 200)]

        self.mocked_context["ssr_ctx"] = {"location": "http://localhost"}

        Template(
            "{% load react %}"
            '{% react_render component="Component" ssr_context=ssr_ctx %}'
        ).render(self.mocked_context)

        request_body = {
            "componentName": "Component",
            "props": {},
            "context": {"location": "http://localhost"},
        }

        self.assertEqual(json.loads(mocked.call_args[1]["data"]), request_body)

    @mock.patch("requests.post")
    def test_default_headers(self, mocked):
        "The SSR uses default headers with json as conten type"
        mocked.side_effect = [MockResponse("Foo Bar", 200)]

        Template("{% load react %}" '{% react_render component="Component" %}').render(
            self.mocked_context
        )

        headers = {
            "Content-type": "application/json",
            "Accept": "text/plain",
        }

        self.assertEqual(mocked.call_count, 1)
        self.assertEqual(mocked.call_args[1]["headers"], headers)

    @override_settings(REACT_RENDER_HEADERS={"Authorization": "Basic 123"})
    @mock.patch("requests.post")
    def test_custom_headers(self, mocked):
        "The SSR uses custom headers if present"
        mocked.side_effect = [MockResponse("Foo Bar", 200)]

        Template("{% load react %}" '{% react_render component="Component" %}').render(
            self.mocked_context
        )

        self.assertTrue(mocked.call_count == 1)
        self.assertEqual(mocked.call_args[1]["headers"]["Authorization"], "Basic 123")

    @mock.patch("requests.post")
    def test_hydrate_if_ssr_present(self, mocked):
        "Makes sure ReactDOM.hydrate is used when SSR is active"
        mocked.side_effect = [MockResponse("Foo Bar", 200)]

        out = Template(
            "{% load react %}"
            '{% react_render component="Component" %}'
            "{% react_print %}"
        ).render(self.mocked_context)

        self.assertTrue("ReactDOM.hydrate(" in out)

    @mock.patch("requests.post")
    def test_ssr_params_are_stored_in_component_queue(self, mocked):
        mocked.side_effect = [MockResponse("Foo Bar", 200)]

        Template("{% load react %}" '{% react_render component="Component" %}').render(
            self.mocked_context
        )

        queue = self.mocked_context["REACT_COMPONENTS"]
        self.assertTrue("ssr_params" in queue[0])
        self.assertEqual(queue[0]["ssr_params"], {})


@override_settings(
    REACT_RENDER_HOST="http://react-service.dev/",
)
class SSRViewTest(SimpleTestCase):
    @mock.patch("django_react_templatetags.ssr.default.SSRService.load_or_empty")
    def test_that_disable_ssr_header_disables_ssr(self, mocked_func):
        self.client.get(
            reverse("static_react_view"),
            HTTP_X_DISABLE_SSR="1",
        )
        self.assertEqual(mocked_func.call_count, 0)


@override_settings(
    REACT_RENDER_HOST="http://react-service.dev/batch",
)
class DefaultServiceTest(SimpleTestCase):
    @mock.patch("requests.post")
    def test_load_or_empty_returns_ok_data(self, mocked):
        mocked.side_effect = [MockResponse("Foo Bar", 200)]

        service = SSRService()
        resp = service.load_or_empty(
            {
                "json": "{}",
                "name": "App",
            }
        )
        self.assertTrue("html" in resp)
        self.assertTrue("Foo Bar" in resp["html"])
        self.assertTrue("params" in resp)
        params = resp["params"]
        self.assertEqual(params, {})
