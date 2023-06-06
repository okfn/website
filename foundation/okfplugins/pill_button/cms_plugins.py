from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cms.models.pluginmodel import CMSPlugin
from django.utils.translation import ugettext_lazy as _

from .models import PillButton

@plugin_pool.register_plugin
class PagePillButtonPlugin(CMSPluginBase):
    model = PillButton
    module = "OKF v2"
    render_template = "pill_button_plugin.html"
    cache = False
    name = _("PillButton")

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)

        return context

