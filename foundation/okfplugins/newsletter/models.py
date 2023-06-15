from django.db import models
from cms.models.pluginmodel import CMSPlugin

class Newsletter(CMSPlugin):
    title = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.title

