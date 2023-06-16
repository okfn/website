from django.db import models
from cms.models.pluginmodel import CMSPlugin


class OKImage(CMSPlugin):
    tag = models.CharField(max_length=200, blank=True)
    image_url = models.ImageField(upload_to='video/images')
    text = models.CharField(max_length=400, default='', blank=True)
    more_text = models.CharField(max_length=400, default='', blank=True)
    url = models.CharField(max_length=400, default='', blank=True)
    caption = models.CharField(max_length=400, default='', blank=True)
    alt = models.CharField(max_length=400, default='', blank=True)
    show_caption = models.BooleanField(default=False)
    in_column = models.BooleanField(default=False)
    in_gallery = models.BooleanField(default=False)

    def __str__(self):
        return self.text
