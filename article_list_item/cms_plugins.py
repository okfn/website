from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cms.models.pluginmodel import CMSPlugin
from django.utils.translation import ugettext_lazy as _

from .models import (ArticleListItemPlugin)

@plugin_pool.register_plugin
class ArticleListItemPlugin(CMSPluginBase):
    model = ArticleListItemPlugin
    name = _("Article list item")
    render_template = "article_list_item_plugin.html"
    cache = False
