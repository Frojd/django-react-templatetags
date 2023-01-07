import logging

from .mock_response import MockResponse

try:
    from unittest import mock
except ImportError:
    import mock

from django.template import Context, Template
from django.test import SimpleTestCase, override_settings

from django_react_templatetags.ssr.hypernova import HypernovaService
from django_react_templatetags.tests.demosite.models import MovieWithContext, Person


@override_settings(
    REACT_RENDER_HOST="http://react-service.dev/batch",
    REACT_SSR_SERVICE="django_react_templatetags.ssr.hypernova.HypernovaService",
)
class HypernovaTemplateTest(SimpleTestCase):
    def setUp(self):
        self.mocked_context = Context({"REACT_COMPONENTS": []})

    @mock.patch("requests.post")
    def test_verify_404(self, mocked):
        "The SSR rendering falls back to client side rendering if 404"

        mocked.side_effect = [MockResponse({"error": "not found"}, 404, ok=False)]

        out = Template(
            "{% load react %}" '{% react_render component="Component" %}'
        ).render(self.mocked_context)

        self.assertTrue('<div id="Component_' in out)

    @mock.patch("requests.post")
    def test_that_only_html_resp_are_shown_in_template(self, mocked):
        mocked.side_effect = [
            MockResponse(
                mock_hypernova_success_response("<h1>Title</h1>"),
                200,
            )
        ]

        out = Template(
            "{% load react %}" '{% react_render component="Component" %}'
        ).render(self.mocked_context)

        self.assertFalse("{'html': " in out)

    @mock.patch("requests.post")
    def test_verify_rendition(self, mocked):
        "The SSR returns inner html"

        mocked.side_effect = [
            MockResponse(
                mock_hypernova_success_response("<h1>Title</h1>"),
                200,
            )
        ]

        out = Template(
            "{% load react %}" '{% react_render component="Component" %}'
        ).render(self.mocked_context)

        self.assertTrue("<h1>Title</h1>" in out)

    @mock.patch("requests.post")
    def test_request_body(self, mocked):
        "The SSR request sends the props in a expected way"

        mocked.side_effect = [
            MockResponse(
                mock_hypernova_success_response("<h1>Title</h1>"),
                200,
            )
        ]

        person = Person(first_name="Tom", last_name="Waits")

        self.mocked_context["person"] = person
        self.mocked_context["component_data"] = {"album": "Real gone"}

        Template(
            "{% load react %}"
            '{% react_render component="Component" prop_person=person data=component_data %}'  # NOQA
        ).render(self.mocked_context)

        request_body = {
            "album": "Real gone",
            "person": {"first_name": "Tom", "last_name": "Waits"},
        }
        self.assertTrue("Component" in mocked.call_args[1]["json"])
        self.assertEqual(mocked.call_args[1]["json"]["Component"]["data"], request_body)

    @mock.patch("requests.post")
    def test_request_body_context(self, mocked):
        "The SSR request sends the props in a expected way with context"

        mocked.side_effect = [
            MockResponse(
                mock_hypernova_success_response("<h1>Title</h1>"),
                200,
            )
        ]

        movie = MovieWithContext(title="Office space", year=1991)

        self.mocked_context["movie"] = movie
        self.mocked_context["search_term"] = "Stapler"

        Template(
            "{% load react %}"
            '{% react_render component="Component" prop_movie=movie %}'
        ).render(self.mocked_context)

        request_body = {
            "movie": {
                "title": "Office space",
                "year": 1991,
                "search_term": "Stapler",
            }
        }

        self.assertTrue("Component" in mocked.call_args[1]["json"])
        self.assertEqual(mocked.call_args[1]["json"]["Component"]["data"], request_body)

    @mock.patch("requests.post")
    def test_default_headers(self, mocked):
        "The SSR uses default headers with json as conten type"
        mocked.side_effect = [
            MockResponse(
                mock_hypernova_success_response("Foo Bar"),
                200,
            )
        ]

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
        mocked.side_effect = [
            MockResponse(
                mock_hypernova_success_response("Foo Bar"),
                200,
            )
        ]

        Template("{% load react %}" '{% react_render component="Component" %}').render(
            self.mocked_context
        )

        self.assertTrue(mocked.call_count == 1)
        self.assertEqual(mocked.call_args[1]["headers"]["Authorization"], "Basic 123")

    @mock.patch("requests.post")
    def test_ssr_params_are_stored_in_component_queue(self, mocked):
        mocked.side_effect = [
            MockResponse(
                mock_hypernova_success_response("Foo Bar"),
                200,
            )
        ]

        Template("{% load react %}" '{% react_render component="Component" %}').render(
            self.mocked_context
        )

        queue = self.mocked_context["REACT_COMPONENTS"]
        self.assertTrue("ssr_params" in queue[0])

        ssr_params = queue[0]["ssr_params"]
        self.assertIn("hypernova_id", ssr_params)
        self.assertIn("hypernova_key", ssr_params)

    @mock.patch("requests.post")
    def test_only_ssr_html_are_returned_on_no_placeholder(self, mocked):
        mocked.side_effect = [
            MockResponse(
                mock_hypernova_success_response("Foo Bar"),
                200,
            )
        ]

        out = Template(
            "{% load react %}"
            '{% react_render component="Component" no_placeholder=1 %}'
        ).render(self.mocked_context)

        queue = self.mocked_context["REACT_COMPONENTS"]
        self.assertEqual(len(queue), 1)
        self.assertFalse(out.startswith('<div id="Component_'))


@override_settings(
    REACT_RENDER_HOST="http://react-service.dev/batch",
    REACT_SSR_SERVICE="django_react_templatetags.ssr.hypernova.HypernovaService",
)
class HypernovaServiceTest(SimpleTestCase):
    @mock.patch("requests.post")
    def test_load_or_empty_returns_ok_data(self, mocked):
        mocked.side_effect = [
            MockResponse(
                mock_hypernova_success_response("Foo Bar", id="my-id", key="App"),
                200,
            )
        ]

        service = HypernovaService()
        resp = service.load_or_empty(
            {
                "json_obj": {},
                "name": "App",
            }
        )
        self.assertTrue("html" in resp)
        self.assertTrue("Foo Bar" in resp["html"])
        self.assertTrue("params" in resp)
        params = resp["params"]
        self.assertTrue("hypernova_id" in params)
        self.assertEqual(params["hypernova_id"], "my-id")
        self.assertTrue("hypernova_key" in params)
        self.assertEqual(params["hypernova_key"], "App")

    @mock.patch("requests.post")
    def test_ssr_context_are_passed_to_hypernova_as_prop(self, mocked):
        mocked.side_effect = [
            MockResponse(
                mock_hypernova_success_response("Foo Bar", id="my-id", key="App"),
                200,
            )
        ]

        service = HypernovaService()
        service.load_or_empty(
            {
                "json_obj": {"month": 4},
                "name": "App",
            },
            ssr_context={
                "language": "en",
            },
        )

        post_data = mocked.call_args[1]["json"]
        self.assertIn("language", post_data["App"]["data"]["context"])
        self.assertEqual(post_data["App"]["data"]["context"]["language"], "en")

    @mock.patch("requests.post")
    def test_empty_html_are_returned_on_request_error(self, mocked):
        logging.disable(logging.CRITICAL)

        mocked.side_effect = [MockResponse("", 500)]

        service = HypernovaService()
        resp = service.load_or_empty(
            {
                "json_obj": {},
                "name": "App",
            }
        )

        self.assertEqual(resp["html"], "")
        self.assertEqual(resp["params"], {})

        logging.disable(logging.NOTSET)


def mock_hypernova_success_response(
    body, component_name="App", id="novaid-1", key="Appjs"
):
    html = (
        '<div data-hypernova-key="{}" data-hypernova-id="{}">'
        "{}".format(key, id, body)
        + "</div>\n"
        + '<script type="application/json" data-hypernova-key="{}" data-hypernova-id="{}">'.format(
            key, id
        )
        + "<!--{}--></script>"
    )  # NOQA

    return {
        "success": True,
        "error": None,
        "results": {
            component_name: {
                "name": component_name,
                "html": html,
                "meta": {},
                "duration": 0.279824,
                "statusCode": 200,
                "success": True,
                "error": None,
            }
        },
    }
