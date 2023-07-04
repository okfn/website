from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import gettext_lazy as _

from .models import List


@plugin_pool.register_plugin
class ListPlugin(CMSPluginBase):
    model = List
    module = "OKF v2"
    render_template = "list_plugin.html"
    cache = False
    name = _("List")

    def render(self, context, instance, placeholder):
        instance.list_items = instance.items.splitlines()
        context = super().render(context, instance, placeholder)

        return context
