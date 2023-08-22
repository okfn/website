from django.db import models
from cms.models.pluginmodel import CMSPlugin

LIST_TYPES = (
    ("long", "Long"),
    ("short", "Short"),
    ("xl", "XL no title"),
)


class List(CMSPlugin):
    title = models.CharField(max_length=500, blank=True)
    items = models.TextField(blank=True)
    list_type = models.CharField(max_length=6, choices=LIST_TYPES, default="long")

    def __str__(self):
        return self.title
