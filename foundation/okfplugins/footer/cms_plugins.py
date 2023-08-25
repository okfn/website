from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import gettext_lazy as _

from .models import FooterModel


@plugin_pool.register_plugin
class FooterPlugin(CMSPluginBase):
    model = FooterModel
    module = "Footer"
    render_template = "footer_plugin.html"
    name = _("Footer")

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)

        return context
