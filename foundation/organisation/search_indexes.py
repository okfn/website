from haystack import indexes
from .models import Person


class PersonIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    twitter = indexes.CharField(model_attr='twitter')
    url = indexes.CharField(model_attr='url')

    def get_model(self):
        return Person
