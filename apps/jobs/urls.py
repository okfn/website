from django.conf.urls import patterns, include, url

from .views import JobListView

urlpatterns = patterns('',
    url(r'^$', JobListView.as_view()),
)
