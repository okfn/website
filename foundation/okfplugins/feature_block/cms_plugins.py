from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import ugettext_lazy as _
from .forms import FeatureBlockForm
from .models import FeatureBlock


@plugin_pool.register_plugin
class FeatureBlockPlugin(CMSPluginBase):
    model = FeatureBlock
    module = "OKF v2"
    render_template = "feature_block_plugin.html"
    cache = False
    name = _("Feature Block")
    form = FeatureBlockForm

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)

        return context
