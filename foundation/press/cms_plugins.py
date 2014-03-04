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
        context = super(RecentPressReleasesPlugin, self)\
            .render(context, instance, placeholder)

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
        context = super(RecentPressMentionsPlugin, self)\
            .render(context, instance, placeholder)

        context['recent_mentions'] = {
            'objects': PressMention.objects.all()[:5]
            }
        return context

plugin_pool.register_plugin(RecentPressMentionsPlugin)
