from django.conf.urls import url

from ..views import WorkingGroupListView

urlpatterns = [
    url(r'^$', WorkingGroupListView.as_view(), name='working-groups'),
]
