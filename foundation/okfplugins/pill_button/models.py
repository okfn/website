from django.db import models
from cms.models.pluginmodel import CMSPlugin


class PillButton(CMSPlugin):
    text = models.CharField(max_length=200)
    url = models.CharField(max_length=200)
    another_window = models.BooleanField(default=False)

    def __str__(self):
        return self.text
