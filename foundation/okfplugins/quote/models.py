from django.db import models
from cms.models.pluginmodel import CMSPlugin

QUOTE_ALIGNMENTS = (
    ("center", "Center"),
    ("left", "Left"),
)


class Quote(CMSPlugin):
    text = models.CharField(max_length=500)
    author = models.CharField(max_length=200, blank=True)
    alignment = models.CharField(
        max_length=6, choices=QUOTE_ALIGNMENTS, default="center"
    )

    def __str__(self):
        return self.text
