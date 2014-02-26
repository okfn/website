from django.conf.urls import patterns, url

from .views import PressReleaseListView, PressReleaseDetailView,\
    PressMentionListView, PressMentionDetailView

urlpatterns = patterns(
    '',
    url(r'^$', PressReleaseListView.as_view(), name='press-releases'),
    url(r'^release/(?P<slug>[^/]+)/$', PressReleaseDetailView.as_view(),
        name='press-release'),
    url(r'^mentions/$', PressMentionListView.as_view(), name='press-mentions'),
    url(r'^mention/(?P<slug>[^/]+)/$', PressMentionDetailView.as_view(),
        name='press-mention'),
    )
