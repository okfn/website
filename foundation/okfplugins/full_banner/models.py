from django.db import models
from cms.models.pluginmodel import CMSPlugin


class FullBanner(CMSPlugin):
    title = models.CharField(max_length=200)
    banner_background = models.ImageField(
        upload_to="banner/images", blank=True, null=True
    )
    banner_picture = models.ImageField(upload_to="banner/images", blank=True, null=True)
    banner_text = models.CharField(max_length=400, default="", blank=True)
    banner_text_strong = models.CharField(max_length=400, default="", blank=True)
    banner_alt = models.CharField(max_length=400, default="", blank=True)
    banner_button_text = models.CharField(max_length=400, default="", blank=True)
    banner_link = models.CharField(max_length=400, default="", blank=True)

    def __str__(self):
        return self.title
