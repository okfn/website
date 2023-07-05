from django.urls import re_path

from ..views import PressReleaseListView, PressReleaseDetailView


urlpatterns = [
    re_path(r'^$', PressReleaseListView.as_view(), name='press-releases'),
    re_path(
        r'^(?P<slug>[^/]+)/$', PressReleaseDetailView.as_view(),
        name='press-release'
    ),
]
