from django.conf.urls import patterns, url

from .views import JobListView

urlpatterns = patterns(
    '',
    url(r'^$', JobListView.as_view(), name='jobs-list'),
    )
