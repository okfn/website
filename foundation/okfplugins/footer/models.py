from django.db import models
from cms.models import CMSPlugin


class FooterModel(CMSPlugin):
    title = models.CharField(max_length=200, blank=True)
    footer = models.TextField(blank=True)

    def __str__(self):
        return self.title
