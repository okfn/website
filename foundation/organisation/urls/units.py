from django.conf.urls import url
from django.views.generic.list import ListView

from ..models import Unit

urlpatterns = [
    url(r'^$', ListView.as_view(model=Unit), name='units'),
]
