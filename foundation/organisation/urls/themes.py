from django.conf.urls import url

from ..views import ThemeDetailView


urlpatterns = [
    url(r'^(?P<slug>[^/]+)/$', ThemeDetailView.as_view(), name='theme'),
]
