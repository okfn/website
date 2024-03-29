from django.db import models
from cms.models.pluginmodel import CMSPlugin


BLOCK_CHOICES = (
    ("yellow_box", "Yellow Box"),
    ("white_box", "White Box"),
    ("transparent_title", "Transparent with Title"),
    ("transparent_no_title", "Transparent without Title"),
    ("background_rounded", "Rounded corners"),
    ("header_background", "Header Background"),
    ("blue", "Blue Background"),
    ("yellow", "Yellow Background"),
    ("purple", "Purple Background"),
)


TEXT_COLOR_CHOICES = (("black", "Black"), ("white", "White"))


class FeatureBlockContainer(CMSPlugin):
    title = models.CharField(max_length=200)
    show_title = models.BooleanField(default=False)

    def __str__(self):
        return self.title


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
    text_color = models.CharField(
        max_length=10, choices=TEXT_COLOR_CHOICES, default="black"
    )

    def __str__(self):
        return self.title
