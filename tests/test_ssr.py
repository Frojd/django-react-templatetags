import json

from django.conf import global_settings
from django.template import Context, Template
from django.test import TestCase, modify_settings, override_settings
import responses

from tests.models import Person, MovieWithContext


@modify_settings(INSTALLED_APPS={'append': 'django_react_templatetags'})
@override_settings(
    MIDDLEWARE=global_settings.MIDDLEWARE,
    TEMPLATES=[{
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': True,
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.core.context_processors.debug',
                'django.core.context_processors.i18n',
                'django.core.context_processors.media',
                'django.core.context_processors.static',
                'django.core.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'django.core.context_processors.request',

                # Project specific
                'django_react_templatetags.context_processors.react_context_processor',  # NOQA
            ],
        },
    }],
    SITE_ID=1,
    REACT_RENDER_HOST='http://react-service.dev/'
)
class SSRTest(TestCase):
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
            }
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
            }
        }

        self.assertTrue(
            json.loads(responses.calls[0].request.body) == request_body
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
