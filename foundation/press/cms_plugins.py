from django.utils.translation import ugettext_lazy as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cms.models.pluginmodel import CMSPlugin

from .models import PressRelease, PressMention


class RecentPressReleasesPlugin(CMSPluginBase):
    model = CMSPlugin
    module = "OKF"
    name = _("Press Releases")
    render_template = "press/pressrelease_recent.html"

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)

        context['recent_releases'] = {
            'objects': PressRelease.published_objects.all()[:5]
        }
        return context


plugin_pool.register_plugin(RecentPressReleasesPlugin)


class RecentPressMentionsPlugin(CMSPluginBase):
    model = CMSPlugin
    module = "OKF"
    name = _("Press Mentions")
    render_template = "press/pressmention_recent.html"

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)

        context['recent_mentions'] = {
            'objects': PressMention.published_objects.all()[:5]
        }
        return context


plugin_pool.register_plugin(RecentPressMentionsPlugin)


class PressResourcePlugin(CMSPluginBase):
    model = CMSPlugin
    module = "OKF"
    name = _("Press Resources")
    render_template = "press/pressresources.html"


plugin_pool.register_plugin(PressResourcePlugin)
