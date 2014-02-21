from django.utils.translation import ugettext_lazy as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cms.models.pluginmodel import CMSPlugin


class SubmenuPlugin(CMSPluginBase):
    model = CMSPlugin
    name = _("Submenu")
    render_template = "cms/plugins/submenu.html"

plugin_pool.register_plugin(SubmenuPlugin)
