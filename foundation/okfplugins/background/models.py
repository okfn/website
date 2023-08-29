from cms.models.pluginmodel import CMSPlugin
from django.db import models

COLOR_CHOICES = (
    ("-bg-circle-okfn-yellow", "Yellow"),
    ("-bg-circle-okfn-green", "Green"),
    ("-bg-circle-okfn-purple", "Purple"),
)

SIZE_CHOICES = (
    ("", "Default"),
    ("-bg-circle-sm", "Small"),
    ("-bg-circle-lg", "Large"),
    ("-bg-circle-xs", "Extra Small"),
    ("-bg-circle-full", "Full"),
)

POSITION_CHOICES = (
    ("default", "Default"),
    ("right", "Right"),
    ("top_left", "Top Left"),
    ("top_right", "Top Right"),
    ("bottom_left", "Bottom Left"),
    ("bottom_right", "Bottom Right"),
)

CSS_POSITION = {
    "default": "",
    "right": "before:top-1/2 before:left-1/2 before:-translate-y-1/2",
    "top_left": "before:-translate-x-1/2 before:-translate-y-1/2",
    "top_right": "before:left-full before:-translate-y-1/2 before:-translate-x-1/2",
    "bottom_right": "before:top-full before:left-full before:-translate-y-1/2 before:-translate-x-1/2",
    "bottom_left": "before:top-full before:right-full before:-translate-y-1/2 before:-translate-x-1/2",
}


class AbstractBackgroundPlugin(CMSPlugin):
    color = models.CharField(max_length=30, choices=COLOR_CHOICES, blank=True)
    size = models.CharField(max_length=30, choices=SIZE_CHOICES, blank=True)
    circle_position = models.CharField(
        max_length=30, choices=POSITION_CHOICES, blank=True
    )

    class Meta:
        abstract = True

    def add_background_variables(self, context):
        context["css_translate"] = CSS_POSITION.get(self.circle_position, "")
        context["has_bg_circle"] = (
            "-has-bg-circle"
            if self.color or self.size or self.circle_position
            else False
        )
