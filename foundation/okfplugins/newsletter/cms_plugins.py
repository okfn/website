from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import ugettext_lazy as _

from .models import Newsletter


@plugin_pool.register_plugin
class NewsletterPlugin(CMSPluginBase):
    model = Newsletter
    module = "OKF v2"
    render_template = "newsletter_plugin.html"
    name = _("Newsletter")

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)

        return context
