from django.conf.urls import patterns, url

from ..views import PressMentionListView, PressMentionDetailView


urlpatterns = patterns(
    '',
    url(r'^$', PressMentionListView.as_view(), name='press-mentions'),
    url(r'^(?P<slug>[^/]+)/$', PressMentionDetailView.as_view(),
        name='press-mention'),
    )
