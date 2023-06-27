from django.db import models
from cms.models.pluginmodel import CMSPlugin


class Video(CMSPlugin):
    title = models.CharField(max_length=200)
    video_image = models.ImageField(upload_to="video/images")
    video_id = models.CharField(max_length=400, default="")
    video_caption = models.CharField(max_length=400, default="")
    video_alt = models.CharField(max_length=400, default="")

    def __str__(self):
        return self.title
