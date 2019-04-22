# -*- coding: utf-8 -*-

from django.conf import global_settings
from django.template import Context, Template
from django.test import TestCase, modify_settings, override_settings
import responses

from django_react_templatetags.templatetags.react import _get_tag_manager, ReactTagManager


class TestReactTagManager(ReactTagManager):
    def render(self, context):
        return 'Test'


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
)
class ReactIncludeComponentTest(TestCase):
    def setUp(self):
        self.mocked_context = Context({'REACT_COMPONENTS': []})

    def test_tag_manager_not_overridden(self):
        "Test that the default ReactTagManager is used by default"
        self.assertEqual(_get_tag_manager(), ReactTagManager)

    @override_settings(
        REACT_RENDER_TAG_MANAGER="django_react_templatetags.tests.test_manager.TestReactTagManager"
    )
    @responses.activate
    def test_tag_manager_overridden(self):
        "Test that the TestReactTagManager is actually used"
        self.assertEqual(_get_tag_manager(), TestReactTagManager)

        responses.add(responses.POST, 'http://react-service.dev',
            body='Foo Bar', status=200)

        out = Template(
            "{% load react %}"
            "{% react_render component=\"Component\" %}"
        ).render(self.mocked_context)

        self.assertEqual('Test', out)
