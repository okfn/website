from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import PressRelease, PressMention

NUM_RECENT_RELEASES = 5
NUM_RECENT_MENTIONS = 5


class PressReleaseListView(ListView):
    model = PressRelease
    paginate_by = 15

    def get_queryset(self):
        return PressRelease.published_objects.all()

    def get_context_data(self, **kwargs):
        context = super(PressReleaseListView, self).get_context_data(**kwargs)

        context['recent_mentions'] = _recent_mentions_context()

        return context


class PressReleaseDetailView(DetailView):
    model = PressRelease

    def get_queryset(self):
        return PressRelease.published_objects.all()

    def get_context_data(self, **kwargs):
        context = super(PressReleaseDetailView, self)\
            .get_context_data(**kwargs)

        context['recent_releases'] = _recent_releases_context(
            context['object'].pk)
        context['recent_mentions'] = _recent_mentions_context()

        return context


class PressMentionListView(ListView):
    model = PressMention
    paginate_by = 15

    def get_queryset(self):
        return PressMention.published_objects.all()

    def get_context_data(self, **kwargs):
        context = super(PressMentionListView, self).get_context_data(**kwargs)

        context['recent_releases'] = _recent_releases_context()

        return context


class PressMentionDetailView(DetailView):
    model = PressMention

    def get_queryset(self):
        return PressMention.published_objects.all()

    def get_context_data(self, **kwargs):
        context = super(PressMentionDetailView, self)\
            .get_context_data(**kwargs)

        context['recent_mentions'] = _recent_mentions_context(
            context['object'].pk)
        context['recent_releases'] = _recent_releases_context()

        return context


def _recent_releases_context(exclude_pk=None):
    objects = PressRelease.published_objects.all()
    if exclude_pk is not None:
        objects = objects.exclude(pk=exclude_pk)
    return {'objects': objects[:NUM_RECENT_RELEASES]}


def _recent_mentions_context(exclude_pk=None):
    objects = PressMention.objects.all()
    if exclude_pk is not None:
        objects = objects.exclude(pk=exclude_pk)
    return {'objects': objects[:NUM_RECENT_MENTIONS]}
