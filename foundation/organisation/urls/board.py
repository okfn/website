from django.conf.urls import url

from ..views import BoardView

urlpatterns = [
    url(r'^$', BoardView.as_view(board='board'), name='board'),
]
