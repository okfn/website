from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cms.models.pluginmodel import CMSPlugin
from django.utils.translation import ugettext_lazy as _

from .models import Header

@plugin_pool.register_plugin
class PageHeaderPlugin(CMSPluginBase):
    model = Header
    render_template = "header_plugin.html"
    cache = False
    name = _("Page Header")

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)

        return context

