from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cms.models.pluginmodel import CMSPlugin
from django.utils.translation import ugettext_lazy as _

from .models import FeatureBlock

@plugin_pool.register_plugin
class FeatureBlockPlugin(CMSPluginBase):
    model = FeatureBlock
    module = "OKF v2"
    render_template = "feature_block_plugin.html"
    cache = False
    name = _("Feature Block")

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)

        return context

