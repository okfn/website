from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import gettext_lazy as _

from .models import Carousel


@plugin_pool.register_plugin
class CarouselPlugin(CMSPluginBase):
    model = Carousel
    module = "OKF v2"
    render_template = "carousel_plugin.html"
    cache = False
    allow_children = True
    name = _("Carousel")
