from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import gettext_lazy as _
from .models import NumberStat, Stat


@plugin_pool.register_plugin
class NumberStatPlugin(CMSPluginBase):
    model = NumberStat
    module = "OKF v2"
    render_template = "number_stat_plugin.html"
    cache = False
    name = _("Number Stat")
    allow_children = True
    child_classes = ["StatPlugin"]

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)

        return context


@plugin_pool.register_plugin
class StatPlugin(CMSPluginBase):
    model = Stat
    module = "OKF v2"
    cache = False
    name = _("Stat")
    render_plugin = False
    require_parent = True
    parent_classes = ["NumberStatPlugin"]
