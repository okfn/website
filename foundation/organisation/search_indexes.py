from haystack import indexes
from .models import Person, NetworkGroup


class PersonIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    twitter = indexes.CharField(model_attr='twitter')
    url = indexes.CharField(model_attr='url')

    def get_model(self):
        return Person

    def get_updated_field(self):
        return 'updated_at'


class NetworkGroupIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    twitter = indexes.CharField(model_attr='twitter')
    homepage_url = indexes.CharField(model_attr='homepage_url')
    mailinglist_url = indexes.CharField(model_attr='mailinglist_url')

    def get_model(self):
        return NetworkGroup

    def get_updated_field(self):
        return 'updated_at'
