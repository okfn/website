from django.db import models
from cms.models.pluginmodel import CMSPlugin

HEADER_CHOICES = (
    ("h1", "Text top / Image left / Long text right"),
    ("h2", "Image right / Two part text left"),
    ("h3", "Image left / Text right"),
)


class Header(CMSPlugin):
    title = models.CharField(max_length=100)
    text = models.CharField(max_length=200)
    second_text = models.CharField(max_length=200, blank=True)
    image_alt = models.CharField(max_length=200)
    image = models.ImageField(upload_to="headers/images", blank=True)
    header_type = models.CharField(max_length=3, choices=HEADER_CHOICES, default="h1")

    def __str__(self):
        return self.title
