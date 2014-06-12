from django.conf.urls import patterns, url

from .views import JobListView, JobHelperView

urlpatterns = patterns(
    '',
    url(r'^$', JobListView.as_view(), name='jobs-list'),
    url(r'^helper/$', JobHelperView.as_view()),
    )
