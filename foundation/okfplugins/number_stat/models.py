from django.db import models
from cms.models.pluginmodel import CMSPlugin

LIST_TYPES = (("single", "Single"), ("multiple", "Multiple"))


class NumberStat(CMSPlugin):
    title = models.CharField(max_length=200)
    columns = models.CharField(max_length=15, choices=LIST_TYPES, default="1")

    def __str__(self):
        return self.title


class Stat(CMSPlugin):
    title = models.CharField(max_length=200)
    stat = models.CharField(max_length=20)
    text = models.CharField(max_length=400, blank=True)
    date = models.CharField(max_length=200, default="", blank=True)
    date_number = models.CharField(max_length=200, default="", blank=True)
    url = models.CharField(max_length=400, default="", blank=True)

    def __str__(self):
        return self.title
