from django.conf.urls import patterns, url

from ..views import NetworkGroupDetailView, networkgroup_csv_output


urlpatterns = patterns(
    '',
    url(r'^(?P<country>[^/]+)/$',
        NetworkGroupDetailView.as_view(),
        name='network-country'),
    url(r'^(?P<country>[^/]+)/(?P<region>[^/]+)/$',
        NetworkGroupDetailView.as_view(),
        name='network-region'),
    url(r'^csv$', networkgroup_csv_output, name='networkgroups-csv'),
    )
