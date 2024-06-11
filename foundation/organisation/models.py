import logging

from cms.models.pluginmodel import CMSPlugin
from cms.extensions import PageExtension
from django.db import models

logger = logging.getLogger(__name__)


class SignupForm(CMSPlugin):
    title = models.CharField(max_length=50, default="Get Connected to Open Knowledge")
    description = models.TextField(blank=True)


class SideBarExtension(PageExtension):
    enabled = models.BooleanField(default=True)
    image = models.ImageField(upload_to="organisation/sidebar/images", blank=True)
