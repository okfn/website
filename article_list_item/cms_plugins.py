from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import gettext_lazy as _
from .forms import ArticleListItemForm
from .models import ArticleListItemPlugin


@plugin_pool.register_plugin
class ArticleListItemPlugin(CMSPluginBase):
    model = ArticleListItemPlugin
    name = _("Article list item")
    render_template = "article_list_item_plugin.html"
    cache = False
    form = ArticleListItemForm
