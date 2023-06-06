from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import ugettext_lazy as _
from .forms import VideoForm
from .models import Video


@plugin_pool.register_plugin
class VideoPlugin(CMSPluginBase):
    model = Video
    module = "OKF v2"
    render_template = "video_plugin.html"
    cache = False
    name = _("Video")
    form = VideoForm

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)

        return context
