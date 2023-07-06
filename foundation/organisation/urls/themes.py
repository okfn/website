from django.urls import re_path

from ..views import ThemeDetailView


urlpatterns = [
    re_path(r'^(?P<slug>[^/]+)/$', ThemeDetailView.as_view(), name='theme'),
]
