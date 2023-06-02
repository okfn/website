from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cms.models.pluginmodel import CMSPlugin
from django.utils.translation import ugettext_lazy as _

from .models import FullBanner

@plugin_pool.register_plugin
class FullBannerPlugin(CMSPluginBase):
    model = FullBanner
    module = "OKF v2"
    render_template = "full_banner_plugin.html"
    cache = False
    name = _("Full Banner")

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)

        return context

