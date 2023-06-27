from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cms.models.pluginmodel import CMSPlugin
from django.utils.translation import ugettext_lazy as _

from .models import BlogOpening


@plugin_pool.register_plugin
class BlogOpeningPlugin(CMSPluginBase):
    model = BlogOpening
    module = "OKF v2"
    render_template = "blog_opening_plugin.html"
    cache = False
    name = _("BlogOpening")
