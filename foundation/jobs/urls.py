from django.conf.urls import url

from .views import JobListView, JobHelperView

urlpatterns = [
    url(r'^$', JobListView.as_view(), name='jobs-list'),
    url(r'^helper/$', JobHelperView.as_view()),
]
