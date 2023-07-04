from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import gettext_lazy as _

from .models import Gallery


@plugin_pool.register_plugin
class GalleryPlugin(CMSPluginBase):
    model = Gallery
    module = "OKF v2"
    render_template = "gallery_plugin.html"
    allow_children = True
    name = _("Gallery")

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)

        return context
