from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import ugettext_lazy as _
from .forms import HeaderForm
from .models import Header


@plugin_pool.register_plugin
class PageHeaderPlugin(CMSPluginBase):
    model = Header
    module = "OKF v2"
    render_template = "header_plugin.html"
    cache = False
    name = _("Page Header")
    form = HeaderForm

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)

        return context
