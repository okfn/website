from django.db import models
from cms.models.pluginmodel import CMSPlugin


class Newsletter(CMSPlugin):
    title = models.CharField(max_length=200, blank=True)
    heading = models.CharField(max_length=200, blank=True)
    text = models.TextField(blank=True)
    button_label = models.CharField(max_length=200, default="Subscribe", blank=True)

    def __str__(self):
        return self.title
