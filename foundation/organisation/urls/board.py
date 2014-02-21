from django.conf.urls import patterns, url

from ..views import BoardView

urlpatterns = patterns(
    '',
    url(r'^$', BoardView.as_view(board='board'), name='board'),
)
