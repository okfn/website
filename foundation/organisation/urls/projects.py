from django.conf.urls import patterns, url

from ..views import ProjectDetailView, ProjectListView


urlpatterns = patterns(
    '',
    url(r'^$', ProjectListView.as_view(), name='projects'),
    url(r'^old$', ProjectListView.as_view(), name='projects_old'),
    url(r'^(?P<slug>[^/]+)/$', ProjectDetailView.as_view(), name='project'),
    )
