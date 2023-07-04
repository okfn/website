from django.urls import re_path

from ..views import WorkingGroupListView

urlpatterns = [
    re_path(r'^$', WorkingGroupListView.as_view(), name='working-groups'),
]
