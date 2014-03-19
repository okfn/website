from django.conf.urls import patterns, url

from ..views import NetworkGroupDetailView


urlpatterns = patterns(
    '',
    url(r'^(?P<country>[^/]+)/$',
        NetworkGroupDetailView.as_view(),
        name='network-country'),
    url(r'^(?P<country>[^/]+)/(?P<region>[^/]+)/$',
        NetworkGroupDetailView.as_view(),
        name='network-region'),
    )
