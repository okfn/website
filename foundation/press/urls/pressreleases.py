from django.conf.urls import url

from ..views import PressReleaseListView, PressReleaseDetailView


urlpatterns = [
    url(r'^$', PressReleaseListView.as_view(), name='press-releases'),
    url(r'^(?P<slug>[^/]+)/$', PressReleaseDetailView.as_view(),
        name='press-release'),
]
