from django.db import models
from cms.models.pluginmodel import CMSPlugin

SPOTLIGHT_ALIGNMENTS = (
    ("center", "Center"),
    ("left", "Left"),
    ("right", "Right"),
)

COLORS = (
    ("black", "Black"),
    ("white", "White")
)


class Spotlight(CMSPlugin):
    title = models.CharField(max_length=500, blank=True)
    text = models.CharField(max_length=500, blank=True)
    button_text = models.CharField(max_length=100, blank=True)
    alignment = models.CharField(
        max_length=6, choices=SPOTLIGHT_ALIGNMENTS, default="center"
    )
    color = models.CharField(max_length=16, choices=COLORS, default="white")
    url = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to="spotlight/images", blank=True)
    image_alt = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return self.title
