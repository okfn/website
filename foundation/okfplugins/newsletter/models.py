from django.db import models
from cms.models.pluginmodel import CMSPlugin

CAMPAIGN_TYPES = (
    ('newsletter', 'Newsletter'),
    ('campaign', 'Campaign'),
    ('small', 'Small')
)

class Newsletter(CMSPlugin):
    title = models.CharField(max_length=200, blank=True)
    heading = models.CharField(max_length=200, blank=True)
    text = models.TextField(blank=True)
    button_label = models.CharField(max_length=200, default="Subscribe", blank=True)
    image = models.ImageField(upload_to="campaign/images", blank=True)
    image_alt = models.CharField(max_length=300, blank=True)
    campaign_type = models.CharField(max_length=20, choices=CAMPAIGN_TYPES, default="newsletter")

    def __str__(self):
        return self.title
