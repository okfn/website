from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import ugettext_lazy as _
from .forms import ArticleLinkForm
from .models import ArticleLink


@plugin_pool.register_plugin
class ArticleLinkPlugin(CMSPluginBase):
    model = ArticleLink
    module = "OKF v2"
    render_template = "article_link_plugin.html"
    cache = False
    name = _("Article Link")
    form = ArticleLinkForm

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)

        return context
