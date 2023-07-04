from django.urls import re_path
from django.utils.text import slugify

from django_countries import countries
from ..views import NetworkGroupDetailView, networkgroup_csv_output


# Generate countries list for the regular expression (it shouldn't be greedy)
COUNTRY_SLUGS = '|'.join([slugify(str(name)) for code, name in countries])


urlpatterns = [
    re_path(r'^(?P<country>' + COUNTRY_SLUGS + r')/$',
        NetworkGroupDetailView.as_view(),
        name='network-country'),
    re_path(r'^(?P<country>' + COUNTRY_SLUGS + r')/(?P<region>[^/]+)/$',
        NetworkGroupDetailView.as_view(),
        name='network-region'),
    re_path(r'^csv$', networkgroup_csv_output, name='networkgroups-csv'),
]
