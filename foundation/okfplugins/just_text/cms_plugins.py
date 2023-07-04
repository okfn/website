from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import gettext_lazy as _

from .models import JustText


@plugin_pool.register_plugin
class PageJustTextPlugin(CMSPluginBase):
    model = JustText
    module = "OKF v2"
    render_template = "just_text_plugin.html"
    cache = False
    name = _("JustText")

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)

        return context
