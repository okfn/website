from django.db import models
from cms.models.pluginmodel import CMSPlugin


BLOCK_CHOICES = (
    ("yellow", "Yellow"),
    ("white", "White"),
    ("transparent_title", "Transparent with Title"),
    ("transparent", "Transparent"),
    ("background_rounded", "Rounded corners"),
    ("blue", "Blue Background"),
    ("yellow", "Yellow Background"),
    ("purple", "Purple Background"),
)


class FeatureBlock(CMSPlugin):
    title = models.CharField(max_length=200, blank=True)
    text = models.CharField(max_length=400, blank=True)
    date = models.CharField(max_length=200, default="", blank=True)
    date_number = models.CharField(max_length=200, default="", blank=True)
    block_type = models.CharField(
        max_length=20, choices=BLOCK_CHOICES, default="yellow"
    )
    image = models.ImageField(upload_to="feature_block/images", blank=True)
    url = models.CharField(max_length=400, blank=True)

    def __str__(self):
        return self.title
