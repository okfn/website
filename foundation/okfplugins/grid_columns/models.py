from django.db import models
from cms.models.pluginmodel import CMSPlugin

class GridColumns(CMSPlugin):
    title = models.CharField(max_length=200)
    columns = models.IntegerField(default=2)

    def __str__(self):
        return self.title

