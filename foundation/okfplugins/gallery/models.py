from django.db import models
from ..background.models import AbstractBackgroundPlugin

GALLERY_TYPES = (("image_slider", "Image Slider"), ("logo_static", "Static Logo"), ("in_column", "In Column"))


class Gallery(AbstractBackgroundPlugin):
    title = models.CharField(max_length=200, blank=True)
    gallery_type = models.CharField(
        max_length=20, choices=GALLERY_TYPES, default="image_slider"
    )
    url = models.CharField(max_length=400, blank=True)
    url_text = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.title
