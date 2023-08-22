from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import gettext_lazy as _
from .forms import FeatureBlockForm
from .models import FeatureBlock, FeatureBlockContainer


@plugin_pool.register_plugin
class FeatureBlockContainerPlugin(CMSPluginBase):
    model = FeatureBlockContainer
    module = "OKF v2"

    cache = False
    allow_children = True
    render_template = "feature_block_container_plugin.html"
    name = _("Feature Block Container")
    child_classes = ["FeatureBlockPlugin"]

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)

        return context


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
