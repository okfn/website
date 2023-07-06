from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import gettext_lazy as _

from .models import Quote


@plugin_pool.register_plugin
class OKQuotePlugin(CMSPluginBase):
    model = Quote
    module = "OKF v2"
    render_template = "quote_plugin.html"
    cache = False
    name = _("Quote")
