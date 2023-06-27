from django.db import models
from cms.models.pluginmodel import CMSPlugin

class HeroPunch(CMSPlugin):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='hero_punch/images')
    image_alt = models.CharField(max_length=200, default='', blank=True)

    def __str__(self):
        return self.title

