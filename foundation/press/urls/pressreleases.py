from django.conf.urls import patterns, url

from ..views import PressReleaseListView, PressReleaseDetailView


urlpatterns = patterns(
    '',
    url(r'^$', PressReleaseListView.as_view(), name='press-releases'),
    url(r'^(?P<slug>[^/]+)/$', PressReleaseDetailView.as_view(),
        name='press-release'),
    )
