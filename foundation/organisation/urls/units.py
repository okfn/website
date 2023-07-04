from django.urls import re_path
from django.views.generic.list import ListView

from ..models import Unit

urlpatterns = [
    re_path(r'^$', ListView.as_view(model=Unit), name='units'),
]
