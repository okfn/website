from django.conf import settings
from django.utils.translation import gettext_lazy as _
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cms.models.pluginmodel import CMSPlugin
from cms.extensions.extension_pool import extension_pool

from .models import (NetworkGroup, NetworkGroupList, WorkingGroup,
                     SideBarExtension)


class NetworkGroupFlagsPlugin(CMSPluginBase):
    model = NetworkGroupList
    module = "OKF"
    name = _("Network Group Flags")
    render_template = "organisation/networkgroup_flags.html"
    text_enabled = True

    def icon_src(self, instance):
        return settings.STATIC_URL + "cms/img/icons/plugins/snippet.png"

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)

        context['title'] = instance.get_group_type_display()
        context['countries'] = NetworkGroup.objects.countries().filter(
            group_type=instance.group_type).order_by('name')

        return context


plugin_pool.register_plugin(NetworkGroupFlagsPlugin)


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
