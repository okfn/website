from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import gettext_lazy as _

from .models import CardPerson


@plugin_pool.register_plugin
class CardPersonPlugin(CMSPluginBase):
    model = CardPerson
    module = "OKF v2"
    name = _("Card Person Plugin")
    render_template = "card_person.html"
    cache = False
