from django.conf.urls import url
from django.utils.text import slugify

from django_countries import countries
from ..views import NetworkGroupDetailView, networkgroup_csv_output


# Generate countries list for the regular expression (it shouldn't be greedy)
COUNTRY_SLUGS = '|'.join([slugify(str(name)) for code, name in countries])


urlpatterns = [
    url(r'^(?P<country>' + COUNTRY_SLUGS + r')/$',
        NetworkGroupDetailView.as_view(),
        name='network-country'),
    url(r'^(?P<country>' + COUNTRY_SLUGS + r')/(?P<region>[^/]+)/$',
        NetworkGroupDetailView.as_view(),
        name='network-region'),
    url(r'^csv$', networkgroup_csv_output, name='networkgroups-csv'),
]
