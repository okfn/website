from django.urls import re_path

from ..views import PressMentionListView, PressMentionDetailView


urlpatterns = [
    re_path(r'^$', PressMentionListView.as_view(), name='press-mentions'),
    re_path(
        r'^(?P<slug>[^/]+)/$', PressMentionDetailView.as_view(),
        name='press-mention'
    ),
]
