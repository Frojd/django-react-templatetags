from django.conf.urls import url


from django_react_templatetags.tests.demosite import views


urlpatterns = [
    url(
        'static-react-view',
        views.StaticReactView.as_view(),
        name='static_react_view',
    ),
]
