from django.db import models
from cms.models.pluginmodel import CMSPlugin

class BlogOpening(CMSPlugin):
    title = models.CharField(max_length=300)
    text = models.CharField(max_length=300)

    def __str__(self):
        return self.title

