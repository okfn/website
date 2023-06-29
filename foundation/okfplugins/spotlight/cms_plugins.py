from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import ugettext_lazy as _

from .models import Spotlight


@plugin_pool.register_plugin
class SpotlightPlugin(CMSPluginBase):
    model = Spotlight
    module = "OKF v2"
    render_template = "spotlight_plugin.html"
    cache = False
    name = _("Spotlight")
