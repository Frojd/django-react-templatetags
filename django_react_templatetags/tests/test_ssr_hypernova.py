import json

from .mock_response import MockResponse

try:
    from unittest import mock
except ImportError:
    import mock

from django.template import Context, Template
from django.test import TestCase, override_settings

from django_react_templatetags.tests.demosite.models import (
    Person, MovieWithContext
)


@override_settings(
    REACT_RENDER_HOST='http://react-service.dev/batch',
    REACT_SSR_SERVICE="django_react_templatetags.ssr.hypernova.HypernovaService",
)

class HypernovaTemplateTest(TestCase):
    def setUp(self):
        self.mocked_context = Context({'REACT_COMPONENTS': []})

    @mock.patch('requests.post')
    def test_verify_404(self, mocked):
        "The SSR rendering falls back to client side rendering if 404"

        mocked.side_effect = [
            MockResponse({'error': 'not found'}, 404, ok=False)
        ]

        out = Template(
            "{% load react %}"
            "{% react_render component=\"Component\" %}"
        ).render(self.mocked_context)

        self.assertTrue('<div id="Component_' in out)

    @mock.patch('requests.post')
    def test_verify_rendition(self, mocked):
        "The SSR returns inner html"

        mocked.side_effect = [
            MockResponse(
                mock_hypernova_success_response('<h1>Title</h1>'),
                200,
            )
        ]

        out = Template(
            "{% load react %}"
            "{% react_render component=\"Component\" %}"
        ).render(self.mocked_context)

        self.assertTrue('<h1>Title</h1>' in out)

    @mock.patch('requests.post')
    def test_request_body(self, mocked):
        "The SSR request sends the props in a expected way"

        mocked.side_effect = [
            MockResponse(
                mock_hypernova_success_response('<h1>Title</h1>'),
                200,
            )
        ]

        person = Person(first_name='Tom', last_name='Waits')

        self.mocked_context["person"] = person
        self.mocked_context["component_data"] = {'album': 'Real gone'}

        Template(
            "{% load react %}"
            "{% react_render component=\"Component\" prop_person=person data=component_data %}"  # NOQA
        ).render(self.mocked_context)

        request_body = {
            "album": "Real gone",
            "person": {
                "first_name": "Tom",
                "last_name": "Waits"
            }
        }
        self.assertTrue('Component' in mocked.call_args[1]["json"])
        self.assertEqual(
            json.loads(mocked.call_args[1]["json"]["Component"]['data']),
            request_body
        )

    @mock.patch('requests.post')
    def test_request_body_context(self, mocked):
        "The SSR request sends the props in a expected way with context"

        mocked.side_effect = [
            MockResponse(
                mock_hypernova_success_response('<h1>Title</h1>'),
                200,
            )
        ]

        movie = MovieWithContext(title='Office space', year=1991)

        self.mocked_context["movie"] = movie
        self.mocked_context["search_term"] = 'Stapler'

        Template(
            "{% load react %}"
            "{% react_render component=\"Component\" prop_movie=movie %}"
        ).render(self.mocked_context)

        request_body = {
            "movie": {
                "title": "Office space",
                "year": 1991,
                "search_term": "Stapler",
            }
        }

        self.assertTrue('Component' in mocked.call_args[1]["json"])
        self.assertEqual(
            json.loads(mocked.call_args[1]["json"]["Component"]['data']),
            request_body
        )

    @mock.patch('requests.post')
    def test_default_headers(self, mocked):
        "The SSR uses default headers with json as conten type"
        mocked.side_effect = [
            MockResponse(
                mock_hypernova_success_response('Foo Bar'),
                200,
            )
        ]

        Template(
            "{% load react %}"
            "{% react_render component=\"Component\" %}"
        ).render(self.mocked_context)

        headers = {
            'Content-type': 'application/json',
            'Accept': 'text/plain',
        }

        self.assertEqual(mocked.call_count, 1)
        self.assertEqual(mocked.call_args[1]["headers"], headers)

    @override_settings(
        REACT_RENDER_HEADERS={
            'Authorization': 'Basic 123'
        }
    )
    @mock.patch('requests.post')
    def test_custom_headers(self, mocked):
        "The SSR uses custom headers if present"
        mocked.side_effect = [
            MockResponse(
                mock_hypernova_success_response('Foo Bar'),
                200,
            )
        ]

        Template(
            "{% load react %}"
            "{% react_render component=\"Component\" %}"
        ).render(self.mocked_context)

        self.assertTrue(mocked.call_count == 1)
        self.assertEqual(mocked.call_args[1]["headers"]['Authorization'], 'Basic 123')


def mock_hypernova_success_response(body, component_name="App"):
    html = "<div data-hypernova-key=\"Appjs\" data-hypernova-id=\"novaid-1\">" \
        "{}".format(body) + \
        "</div>\n" + \
        "<script type=\"application/json\" data-hypernova-key=\"Appjs\" data-hypernova-id=\"novaid-1\"><!--{}--></script>"  # NOQA

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
        }
    }
