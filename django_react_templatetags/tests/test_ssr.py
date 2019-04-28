import json
try:
    from unittest import mock
except ImportError:
    import mock

from django.urls import reverse
from django.template import Context, Template
from django.test import TestCase, override_settings
import responses

from django_react_templatetags.tests.demosite.models import (
    Person, MovieWithContext
)


@override_settings(
    REACT_RENDER_HOST='http://react-service.dev/',
)
class SSRTemplateTest(TestCase):
    def setUp(self):
        self.mocked_context = Context({'REACT_COMPONENTS': []})

    @responses.activate
    def test_verify_404(self):
        "The SSR rendering falls back to client side rendering if 404"
        responses.add(responses.POST, 'http://react-service.dev/',
                      json={'error': 'not found'}, status=404)

        out = Template(
            "{% load react %}"
            "{% react_render component=\"Component\" %}"
        ).render(self.mocked_context)

        self.assertTrue('<div id="Component_' in out)

    @responses.activate
    def test_verify_rendition(self):
        "The SSR returns inner html"
        responses.add(responses.POST, 'http://react-service.dev',
                      body='<h1>Title</h1>', status=200)

        out = Template(
            "{% load react %}"
            "{% react_render component=\"Component\" %}"
        ).render(self.mocked_context)

        self.assertTrue('<h1>Title</h1>' in out)

    @responses.activate
    def test_request_body(self):
        "The SSR request sends the props in a expected way"

        responses.add(responses.POST, 'http://react-service.dev',
                      body='<h1>Title</h1>', status=200)

        person = Person(first_name='Tom', last_name='Waits')

        self.mocked_context["person"] = person
        self.mocked_context["component_data"] = {'album': 'Real gone'}

        Template(
            "{% load react %}"
            "{% react_render component=\"Component\" prop_person=person data=component_data %}"  # NOQA
        ).render(self.mocked_context)

        request_body = {
            'componentName': 'Component',
            'props': {
                'album': 'Real gone',
                'person': {
                    'first_name': 'Tom',
                    'last_name': 'Waits'
                }
            },
            'context': {}
        }

        self.assertTrue(
            json.loads(responses.calls[0].request.body) == request_body
        )

    @responses.activate
    def test_request_body_context(self):
        "The SSR request sends the props in a expected way with context"

        responses.add(responses.POST, 'http://react-service.dev',
                      body='<h1>Title</h1>', status=200)

        movie = MovieWithContext(title='Office space', year=1991)

        self.mocked_context["movie"] = movie
        self.mocked_context["search_term"] = 'Stapler'

        Template(
            "{% load react %}"
            "{% react_render component=\"Component\" prop_movie=movie %}"
        ).render(self.mocked_context)

        request_body = {
            'componentName': 'Component',
            'props': {
                'movie': {
                    'title': 'Office space',
                    'year': 1991,
                    'search_term': 'Stapler',
                }
            },
            'context': {}
        }

        self.assertEquals(
            json.loads(responses.calls[0].request.body),
            request_body
        )

    @responses.activate
    def test_request_body_with_ssr_context(self):
        "The SSR request appends the 'ssr_context' in an expected way"

        responses.add(responses.POST, 'http://react-service.dev',
                      body='<h1>Title</h1>', status=200)

        self.mocked_context["ssr_ctx"] = {"location": "http://localhost"}

        Template(
            "{% load react %}"
            "{% react_render component=\"Component\" ssr_context=ssr_ctx %}"
        ).render(self.mocked_context)

        request_body = {
            'componentName': 'Component',
            'props': {},
            'context': {'location': "http://localhost"}
        }

        self.assertEquals(
            json.loads(responses.calls[0].request.body),
            request_body
        )

    @responses.activate
    def test_default_headers(self):
        "The SSR uses default headers with json as conten type"
        responses.add(responses.POST, 'http://react-service.dev',
                      body='Foo Bar', status=200)

        Template(
            "{% load react %}"
            "{% react_render component=\"Component\" %}"
        ).render(self.mocked_context)

        self.assertTrue(len(responses.calls) == 1)
        self.assertEquals(
            responses.calls[0].request.headers['Content-type'],
            'application/json'
        )
        self.assertEquals(
            responses.calls[0].request.headers['Accept'],
            'text/plain'
        )

    @override_settings(
        REACT_RENDER_HEADERS={
            'Authorization': 'Basic 123'
        }
    )
    @responses.activate
    def test_custom_headers(self):
        "The SSR uses custom headers if present"
        responses.add(responses.POST, 'http://react-service.dev',
                      body='Foo Bar', status=200)

        Template(
            "{% load react %}"
            "{% react_render component=\"Component\" %}"
        ).render(self.mocked_context)

        self.assertTrue(len(responses.calls) == 1)
        self.assertEquals(
            responses.calls[0].request.headers['Authorization'],
            'Basic 123'
        )

    @responses.activate
    def test_hydrate_if_ssr_present(self):
        "Makes sure ReactDOM.hydrate is used when SSR is active"
        responses.add(responses.POST, 'http://react-service.dev',
                      body='Foo Bar', status=200)

        out = Template(
            "{% load react %}"
            "{% react_render component=\"Component\" %}"
            "{% react_print %}"
        ).render(self.mocked_context)

        self.assertTrue('ReactDOM.hydrate(' in out)


@override_settings(
    REACT_RENDER_HOST='http://react-service.dev/',
)
class SSRViewTest(TestCase):
    @mock.patch("django_react_templatetags.ssr.SSRService.load_or_empty")
    def test_that_disable_ssr_header_disables_ssr(self, mocked_func):
        self.client.get(
            reverse('static_react_view'),
            HTTP_X_DISABLE_SSR='1',
        )
        self.assertEqual(mocked_func.call_count, 0)



class CustomSSRService():
    def load_or_empty(self, component, headers={}, ssr_context=None):
        pass


@override_settings(
    REACT_RENDER_HOST='http://react-service.dev/',
    REACT_SSR_SERVICE="django_react_templatetags.tests.test_ssr.CustomSSRService",
)
class CustomSSRServiceTest(TestCase):
    @mock.patch("django_react_templatetags.tests.test_ssr.CustomSSRService.load_or_empty")
    def test_that_disable_ssr_header_disables_ssr(self, mocked_func):
        self.client.get(
            reverse('static_react_view'),
        )
        self.assertEqual(mocked_func.call_count, 1)
