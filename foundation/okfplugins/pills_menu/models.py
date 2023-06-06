from django.db import models
from cms.models.pluginmodel import CMSPlugin

class PillsMenu(CMSPlugin):
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title

