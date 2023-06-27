from django.db import models
from cms.models.pluginmodel import CMSPlugin


class JustText(CMSPlugin):
    text = models.TextField(max_length=200)

    def __str__(self):
        return self.text
