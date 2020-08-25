from django.conf.urls import url

from ..views import ProjectDetailView, ProjectListView


urlpatterns = [
    url(r'^$', ProjectListView.as_view(), name='projects'),
    url(r'^old$', ProjectListView.as_view(), name='projects_old'),
    url(r'^(?P<slug>[^/]+)/$', ProjectDetailView.as_view(), name='project'),
]
