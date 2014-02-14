from django.conf.urls import *

from ..views import BoardView


urlpatterns = patterns('',
    url(r'^$', BoardView.as_view(board='board'), name='board'),
)            
