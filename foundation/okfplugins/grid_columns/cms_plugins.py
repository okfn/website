from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cms.models.pluginmodel import CMSPlugin
from django.utils.translation import ugettext_lazy as _

from .models import GridColumns

@plugin_pool.register_plugin
class GridColumnsPlugin(CMSPluginBase):
    model = GridColumns
    module = "OKF v2"
    render_template = "grid_columns_plugin.html"
    cache = False
    allow_children = True
    name = _("Grid Columns")

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)

        return context

