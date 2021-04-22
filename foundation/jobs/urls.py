from django.conf.urls import url

from .views import JobListView

urlpatterns = [
    url(r'^$', JobListView.as_view(), name='jobs-list'),
]
