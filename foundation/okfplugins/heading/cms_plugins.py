from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cms.models.pluginmodel import CMSPlugin
from django.utils.translation import ugettext_lazy as _

from .models import Heading

@plugin_pool.register_plugin
class PageHeadingPlugin(CMSPluginBase):
    model = Heading
    module = "OKF v2"
    render_template = "heading_plugin.html"
    cache = False
    name = _("Heading")

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)

        return context

