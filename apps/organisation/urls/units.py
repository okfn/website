from django.conf.urls import patterns, url
from django.views.generic.list import ListView

from ..models import Unit

urlpatterns = patterns(
    '',
    url(r'^$', ListView.as_view(model=Unit), name='units'),
)
