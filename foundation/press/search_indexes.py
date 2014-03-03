from django.utils import timezone
from haystack import indexes
from .models import PressRelease, PressMention


class PressReleaseIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return PressRelease

    def index_queryset(self, using=None):
        return self.get_model().published_objects.all()


class PressMentionIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    publisher = indexes.CharField(model_attr='publisher')
    url = indexes.CharField(model_attr='url')

    def get_model(self):
        return PressMention
