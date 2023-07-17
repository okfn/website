from django.urls import re_path

from ..views import ProjectDetailView


urlpatterns = [
    re_path(r'^(?P<slug>[^/]+)/$', ProjectDetailView.as_view(), name='project'),
]
