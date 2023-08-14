from django.db import models
from cms.models.pluginmodel import CMSPlugin

BANNER_CHOICES = (
    ("warning", "warning"),
    ("success", "success"),
    ("error", "error"),
    ("info", "info"),
)


class Banner(CMSPlugin):
    title = models.CharField(max_length=200)
    text = models.TextField()
    banner_type = models.CharField(max_length=20, choices=BANNER_CHOICES, default="")

    def __str__(self):
        return self.title
