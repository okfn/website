from django.db import models
from cms.models.pluginmodel import CMSPlugin

LIST_TYPES = (
    ("default", "Default"),
    ("opening_default", "Opening Default"),
    ("opening_center", "Opening Center"),
)


class HeroPunch(CMSPlugin):
    title = models.CharField(max_length=200)
    text = models.CharField(max_length=400, blank=True)
    image = models.ImageField(upload_to="hero_punch/images")
    image_alt = models.CharField(max_length=200, default="", blank=True)
    banner_type = models.CharField(max_length=15, choices=LIST_TYPES, default="default")
    url = models.CharField(max_length=400, blank=True)
    url_text = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.title
