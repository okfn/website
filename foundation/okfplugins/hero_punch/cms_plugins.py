from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import ugettext_lazy as _

from .models import HeroPunch


@plugin_pool.register_plugin
class HeroPunchPlugin(CMSPluginBase):
    model = HeroPunch
    module = "OKF v2"
    render_template = "hero_punch_plugin.html"
    cache = False
    name = _("HeroPunch")
