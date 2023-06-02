from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cms.models.pluginmodel import CMSPlugin
from django.utils.translation import ugettext_lazy as _

from .models import PillsMenu

@plugin_pool.register_plugin
class PillsMenuPlugin(CMSPluginBase):
    model = PillsMenu
    module = "OKF v2"
    render_template = "pills_menu_plugin.html"
    cache = False
    allow_children = True
    name = _("Pills Menu")

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)

        return context

