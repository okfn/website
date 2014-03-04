from django.utils.translation import ugettext_lazy as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .models import FeaturedProject


class FeaturedProjectPlugin(CMSPluginBase):
    model = FeaturedProject
    name = _("Featured Project")
    render_template = "organisation/project_featured.html"

    def render(self, context, instance, placeholder):
        context = super(FeaturedProjectPlugin, self)\
            .render(context, instance, placeholder)

        context['project'] = instance.project
        return context

plugin_pool.register_plugin(FeaturedProjectPlugin)
