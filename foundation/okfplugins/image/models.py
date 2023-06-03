from django.db import models
from cms.models.pluginmodel import CMSPlugin

class OKImage(CMSPlugin):
    tag = models.CharField(max_length=200)
    image_url = models.ImageField(upload_to='video/images')
    text = models.CharField(max_length=400, default='')
    more_text = models.CharField(max_length=400, default='')
    url = models.CharField(max_length=400, default='')
    caption = models.CharField(max_length=400, default='')
    alt = models.CharField(max_length=400, default='')

    def __str__(self):
        return self.text

