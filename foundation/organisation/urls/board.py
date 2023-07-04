from django.urls import re_path

from ..views import BoardView

urlpatterns = [
    re_path(r'^$', BoardView.as_view(board='our-board'), name='board'),
]
