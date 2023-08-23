from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import gettext_lazy as _

from .models import GridColumns


@plugin_pool.register_plugin
class GridColumnsPlugin(CMSPluginBase):

    _class_mapping = {
        1: "md:grid-cols-1",
        2: "md:grid-cols-2",
        3: "md:grid-cols-3",
        4: "md:grid-cols-4",
        5: "md:grid-cols-5",
        6: "md:grid-cols-6",
        7: "md:grid-cols-7",
        8: "md:grid-cols-8",
        9: "md:grid-cols-9",
        10: "md:grid-cols-10",
        11: "md:grid-cols-11",
        12: "md:grid-cols-12"
    }

    model = GridColumns
    module = "OKF v2"
    render_template = "grid_columns_plugin.html"
    cache = False
    allow_children = True
    name = _("Grid Columns")

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        context['grid_cols_class'] = self._class_mapping[instance.columns]
        context['skip_columns'] = range(instance.skip_columns)
        return context
