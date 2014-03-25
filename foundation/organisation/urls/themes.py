from django.conf.urls import patterns, url

from ..views import ThemeDetailView


urlpatterns = patterns(
    '',
    url(r'^(?P<slug>[^/]+)/$', ThemeDetailView.as_view(), name='theme'),
    )
