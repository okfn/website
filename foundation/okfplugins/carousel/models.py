from django.db import models
from cms.models.pluginmodel import CMSPlugin


class Carousel(CMSPlugin):
    title = models.CharField(max_length=500)

    def __str__(self):
        return self.title
