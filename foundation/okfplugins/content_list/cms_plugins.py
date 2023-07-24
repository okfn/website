from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import gettext_lazy as _
from .models import ContentList


@plugin_pool.register_plugin
class ContentListPlugin(CMSPluginBase):
    model = ContentList
    module = "OKF v2"
    render_template = "content_list_plugin.html"
    cache = False
    name = _("Content List")

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)

        return context
