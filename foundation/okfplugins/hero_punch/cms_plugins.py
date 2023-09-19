from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import gettext_lazy as _

from .models import HeroPunch
from .forms import HeroPunchForm


@plugin_pool.register_plugin
class HeroPunchPlugin(CMSPluginBase):
    model = HeroPunch
    module = "OKF v2"
    render_template = "hero_punch_plugin.html"
    cache = False
    name = _("HeroPunch")
    form = HeroPunchForm
