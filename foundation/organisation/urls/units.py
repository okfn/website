from django.urls import re_path
from django.views.generic.list import ListView

from ..models import Unit
from ..views import PersonView

urlpatterns = [
    re_path(r'^$', ListView.as_view(model=Unit), name='units'),
    re_path(r'^(?P<person_id>\d+)/$', PersonView.as_view(), name='person')
]
