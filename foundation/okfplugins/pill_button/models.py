from django.db import models
from cms.models.pluginmodel import CMSPlugin

BUTTON_TYPE = (
    ("black", "Black"),
    ("white", "White"),
    ("pill", "Pill"),
    ("subtitle", "Subtitle"),
    ("subtitle_large", "Subtitle large"),
    ("arrow", "Arrow"),
)


class PillButton(CMSPlugin):
    text = models.CharField(max_length=200)
    url = models.CharField(max_length=200, blank=True)
    another_window = models.BooleanField(default=False)
    button_type = models.CharField(max_length=16, choices=BUTTON_TYPE, default="pill")

    def __str__(self):
        return self.text
