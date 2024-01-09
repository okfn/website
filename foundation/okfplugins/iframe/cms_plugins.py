from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .models import IFramePlugin

@plugin_pool.register_plugin
class IFramePlugin(CMSPluginBase):
    model = IFramePlugin
    render_template = "iframe_plugin.html"
    cache = False
    module = "OKF v2"
