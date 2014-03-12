from haystack import indexes
from .models import Person, Project, WorkingGroup


class PersonIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    twitter = indexes.CharField(model_attr='twitter')
    url = indexes.CharField(model_attr='url')

    def get_model(self):
        return Person


class ProjectIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    twitter = indexes.CharField(model_attr='twitter')
    homepage_url = indexes.CharField(model_attr='homepage_url')
    mailinglist_url = indexes.CharField(model_attr='mailinglist_url')
    sourcecode_url = indexes.CharField(model_attr='sourcecode_url')

    def get_model(self):
        return Project


class WorkingGroupIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    incubation = indexes.BooleanField(model_attr='incubation')

    def get_model(self):
        return WorkingGroup
