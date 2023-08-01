from django.db import models
from cms.models.pluginmodel import CMSPlugin


class ContentList(CMSPlugin):
    title = models.CharField(max_length=200)
    text = models.CharField(max_length=400, blank=True)
    date = models.CharField(max_length=200, default="", blank=True)
    date_number = models.CharField(max_length=200, default="", blank=True)
    url = models.CharField(max_length=400, default="", blank=True)

    def __str__(self):
        return self.title
