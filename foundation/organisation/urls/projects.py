from django.conf.urls import patterns, url

from ..views import ProjectDetailView, ProjectListView


urlpatterns = patterns(
    '',
    url(r'^$', ProjectListView.as_view(), name='projects'),
    url(r'^(?P<slug>[^/]+)/$', ProjectDetailView.as_view(), name='project'),
    )
