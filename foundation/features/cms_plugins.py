from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cms.models.pluginmodel import CMSPlugin
from django.utils.translation import gettext_lazy as _

from .models import Feature


class FeaturePlugin(CMSPluginBase):
    model = CMSPlugin
    render_template = "feature_plugin.html"
    cache = True
    module = "OKF"
    name = _("Featured News")

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)

        context['feature_list'] = Feature.objects.filter(published=True).order_by('order', 'title')
        return context


plugin_pool.register_plugin(FeaturePlugin)
