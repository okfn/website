from django.conf.urls import *

from django.views.generic.list import ListView

from .views import BoardView
from .models import Unit

urlpatterns = patterns('',
    url(r'^team/$', ListView.as_view(model=Unit), name='units'),
    url(r'^board/$', BoardView.as_view(board='board'), name='board'),
    url(r'^advisory-board/$', BoardView.as_view(board='advisory-board'),
        name='advisory-board'),
)
            
