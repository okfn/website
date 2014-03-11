from django.conf.urls import patterns, url

from ..views import WorkingGroupListView

urlpatterns = patterns(
    '',
    url(r'^$', WorkingGroupListView.as_view(), name='working-groups'),
    )
