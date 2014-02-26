from django.utils import timezone
from django.core.urlresolvers import reverse

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import PressRelease, PressMention


class PressReleaseListView(ListView):
    model = PressRelease

    def get_queryset(self):
        return PressRelease.objects.filter(release_date__lt=timezone.now())

    def get_context_data(self, **kwargs):
        context = super(PressReleaseListView, self).get_context_data(**kwargs)
        context['sidebar_recent'] = {
            'objects': PressMention.objects.all()[:5],
            'fulllist': reverse('press-mentions')
            }
        return context


class PressReleaseDetailView(DetailView):
    model = PressRelease

    def get_context_data(self, **kwargs):
        context = super(PressReleaseDetailView, self).get_context_data(**kwargs)
        context['sidebar_recent'] = {
            'releases': PressRelease.objects\
                .exclude(pk=context['object'].pk)\
                .filter(release_date__lt=timezone.now())[:5],
            'mentions': PressMention.objects.all()[:5]
            }
        return context


class PressMentionListView(ListView):

    model = PressMention

    def get_context_data(self, **kwargs):
        context = super(PressMentionListView, self).get_context_data(**kwargs)
        context['sidebar_recent'] = {
            'objects': PressRelease.objects.all()[:5],
            'fulllist': reverse('press-releases')
            }
        return context


class PressMentionDetailView(DetailView):
    model = PressMention

    def get_context_data(self, **kwargs):
        context = super(PressMentionDetailView, self).get_context_data(**kwargs)
        context['sidebar_recent'] = {
            'mentions': PressMention.objects\
                .exclude(pk=context['object'].pk)[:5],
            'releases': PressRelease.objects\
                .filter(release_date__lt=timezone.now())[:5]
            }
        return context
