from django.db import models
from cms.models.pluginmodel import CMSPlugin

class ArticleLink(CMSPlugin):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    image = models.ImageField(upload_to='article/images', blank=True)

    def __str__(self):
        return self.title

