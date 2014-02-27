from django.utils import timezone
from django.core.urlresolvers import reverse

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import PressRelease, PressMention


class PressReleaseListView(ListView):
    model = PressRelease
    paginate_by = 15

    def get_queryset(self):
        return PressRelease.objects.filter(release_date__lt=timezone.now())

    def get_context_data(self, **kwargs):
        context = super(PressReleaseListView, self).get_context_data(**kwargs)

        context['recent_mentions'] = {
            'objects': PressMention.objects.all()[:5],
            }

        return context


class PressReleaseDetailView(DetailView):
    model = PressRelease

    def get_queryset(self):
        return PressRelease.objects.filter(release_date__lt=timezone.now())

    def get_context_data(self, **kwargs):
        context = super(PressReleaseDetailView, self)\
            .get_context_data(**kwargs)

        context['recent_releases'] = {
            'objects': PressRelease.objects
            .exclude(pk=context['object'].pk)
            .filter(release_date__lt=timezone.now())[:5]
            }
        context['recent_mentions'] = {
            'objects': PressMention.objects.all()[:5]
            }

        return context


class PressMentionListView(ListView):
    model = PressMention
    paginate_by = 15

    def get_context_data(self, **kwargs):
        context = super(PressMentionListView, self).get_context_data(**kwargs)

        context['recent_releases'] = {
            'objects': PressRelease.objects.all()[:5],
            }

        return context


class PressMentionDetailView(DetailView):
    model = PressMention

    def get_context_data(self, **kwargs):
        context = super(PressMentionDetailView, self)\
            .get_context_data(**kwargs)

        context['recent_mentions'] = {
            'objects': PressMention.objects
            .exclude(pk=context['object'].pk)[:5]
            }
        context['recent_releases'] = {
            'objects': PressRelease.objects
            .filter(release_date__lt=timezone.now())[:5]
            }

        return context
