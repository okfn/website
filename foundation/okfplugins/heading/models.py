from django.db import models
from cms.models.pluginmodel import CMSPlugin

HEADINGS_CHOICES = (
    ("h0", "h1"),
    ("h1", "h2"),
    ("h2", "h3"),
    ("h3", "h4"),
    ("h4", "h5"),
    ("h5", "h6"),
)

HEADINGS_ALIGNMENTS = (("center", "Center"), ("left", "Left"), ("right", "Right"))


class Heading(CMSPlugin):
    title = models.CharField(max_length=200)
    heading_type = models.CharField(
        max_length=3, choices=HEADINGS_CHOICES, default="h1"
    )
    highlighted = models.BooleanField(default=False)
    alignment = models.CharField(
        max_length=6, choices=HEADINGS_ALIGNMENTS, default="center"
    )

    def __str__(self):
        return self.title
