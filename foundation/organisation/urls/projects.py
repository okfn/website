from django.urls import re_path

from ..views import ProjectDetailView, ProjectListView


urlpatterns = [
    re_path(r'^$', ProjectListView.as_view(), name='projects'),
    re_path(r'^old$', ProjectListView.as_view(), name='projects_old'),
    re_path(r'^(?P<slug>[^/]+)/$', ProjectDetailView.as_view(), name='project'),
]
