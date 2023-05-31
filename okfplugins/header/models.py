from django.db import models
from cms.models.pluginmodel import CMSPlugin


class Header(CMSPlugin):
    title = models.CharField(max_length=100)
    text = models.CharField(max_length=200)
    image_alt = models.CharField(max_length=200)
    image = models.ImageField(upload_to='headers/images', blank=True)

    def __str__(self):
        return self.title

