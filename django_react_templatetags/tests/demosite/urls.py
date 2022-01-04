from django.urls import path

from django_react_templatetags.tests.demosite import views

urlpatterns = [
    path(
        "static-react-view",
        views.StaticReactView.as_view(),
        name="static_react_view",
    ),
]
