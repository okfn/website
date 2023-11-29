from cms.models.pluginmodel import CMSPlugin

from django.db import models

class CardPerson(CMSPlugin):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    photo = models.ImageField(upload_to="card_person/photos", blank=True)
    email = models.EmailField(blank=True)
    url = models.URLField(blank=True)
    x_account = models.CharField(max_length=18, blank=True)
