from django.utils.translation import ugettext_lazy as _

from cms.plugin_pool import plugin_pool
from cms.plugin_base import CMSPluginBase

from .models import Quote
from .forms import QuotePluginForm


class QuotePlugin(CMSPluginBase):
    render_template = False
    model = Quote
    name = _('Quote')
    form = QuotePluginForm
    fields = ('style', 'content', 'footer', 'url', 'target',)

    def render(self, context, instance, placeholder):
        self.render_template = 'aldryn_quote/plugins/%s/quote.html' % instance.style
        context.update({
            'quote': instance.content,
            'footer': instance.footer,
            'url': instance.url,
            'target': instance.target,
            'object': instance,
            'placeholder': placeholder
        })
        return context


plugin_pool.register_plugin(QuotePlugin)