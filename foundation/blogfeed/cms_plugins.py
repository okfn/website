from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cms.models.pluginmodel import CMSPlugin
from django.utils.translation import ugettext_lazy as _
import feedparser


class FeedDisplayPlugin(CMSPluginBase):
    model = CMSPlugin
    render_template = "hello_plugin.html"
    cache = False
    module = "OKF"
    name = _("Latest Blogposts")

    def _get_three_articles(self):
        feed_url = 'https://blog.okfn.org/?feed=enclosure'
        feed = feedparser.parse(feed_url)
        return feed.entries[:3]

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        context['entries'] = self._get_three_articles()
        return context


plugin_pool.register_plugin(FeedDisplayPlugin)
