from django.conf import settings
from django.utils.translation import gettext_lazy as _
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cms.models.pluginmodel import CMSPlugin
from cms.extensions.extension_pool import extension_pool

from .models import WorkingGroup, SideBarExtension


class WorkingGroupPlugin(CMSPluginBase):
    model = CMSPlugin
    module = "OKF"
    name = _("Working Groups")
    render_template = "organisation/workinggroup_shortlist.html"
    text_enabled = True

    def icon_alt(self, instance):
        return 'Working Groups'

    def icon_src(self, instance):
        return settings.STATIC_URL + "cms/img/icons/plugins/snippet.png"

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)

        context['workinggroups'] = WorkingGroup.objects.active()
        return context


plugin_pool.register_plugin(WorkingGroupPlugin)

extension_pool.register(SideBarExtension)
