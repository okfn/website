from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import gettext_lazy as _

from .models import Banner


@plugin_pool.register_plugin
class BannerPlugin(CMSPluginBase):
    model = Banner
    module = "OKF v2"
    render_template = "banner_plugin.html"
    cache = False
    name = _("Banner")

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)

        return context
