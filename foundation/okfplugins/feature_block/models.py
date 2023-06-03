from django.db import models
from cms.models.pluginmodel import CMSPlugin

BLOCK_CHOICES = (
    ('yellow','Yellow'),
    ('white', 'White'),
    ('transparent','Transparent'),
)

class FeatureBlock(CMSPlugin):
    title = models.CharField(max_length=200)
    text = models.CharField(max_length=400)
    date = models.CharField(max_length=200, default='')
    date_number = models.CharField(max_length=200, default='')
    block_type = models.CharField(max_length=20, choices=BLOCK_CHOICES, default='yellow')
    image = models.ImageField(upload_to='feature_block/images', blank=True)
    url = models.CharField(max_length=400)

    def __str__(self):
        return self.title

