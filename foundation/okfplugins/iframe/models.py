from django.db import models
from cms.models.pluginmodel import CMSPlugin


class IFramePlugin(CMSPlugin):
    """
    Plugin for embedding an iframe
    """
    src = models.URLField()
    width = models.CharField(max_length=10, default='100%', help_text='e.g. 100% or 500px')
    height = models.CharField(max_length=10, default='100%', help_text='e.g. 100% or 500px')
    style = models.CharField(max_length=100, blank=True, help_text='e.g. border: 1px solid black;')

    class Meta:
        verbose_name = 'iframe'
        verbose_name_plural = 'iframes'

    def __unicode__(self):
        return f"iframe: {self.src}"
