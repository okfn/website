from django.utils.translation import ugettext_lazy as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cms.models.pluginmodel import CMSPlugin

from sorl.thumbnail import get_thumbnail

from .models import (Project, Theme, FeaturedTheme, FeaturedProject,
                     ProjectList, NetworkGroup, SignupForm)


class FeaturedThemePlugin(CMSPluginBase):
    model = FeaturedTheme
    module = "OKF"
    name = _("Featured Theme")
    text_enabled = True
    render_template = "organisation/theme_featured.html"

    def icon_alt(self, instance):
        return 'Theme: %s' % instance.theme.name

    def icon_src(self, instance):
        im = get_thumbnail(instance.theme.picture, '50x50', quality=99)
        return im.url

    def render(self, context, instance, placeholder):
        context = super(FeaturedThemePlugin, self)\
            .render(context, instance, placeholder)

        context['object'] = instance.theme
        return context

plugin_pool.register_plugin(FeaturedThemePlugin)


class FeaturedProjectPlugin(CMSPluginBase):
    model = FeaturedProject
    module = "OKF"
    name = _("Featured Project")
    render_template = "organisation/project_featured.html"

    def render(self, context, instance, placeholder):
        context = super(FeaturedProjectPlugin, self)\
            .render(context, instance, placeholder)

        context['project'] = instance.project
        return context

plugin_pool.register_plugin(FeaturedProjectPlugin)


class ProjectListPlugin(CMSPluginBase):
    model = ProjectList
    module = "OKF"
    name = _("Project List")
    render_template = "organisation/project_list_plugin.html"

    def render(self, context, instance, placeholder):
        context = super(ProjectListPlugin, self)\
            .render(context, instance, placeholder)

        results = Project.objects.all()

        if instance.theme:
            results = results.filter(themes=instance.theme)

        if instance.project_type:
            results = results.filter(types=instance.project_type)

        context['projects'] = results
        return context

plugin_pool.register_plugin(ProjectListPlugin)


class ThemesPlugin(CMSPluginBase):
    model = CMSPlugin
    module = "OKF"
    name = _("Theme list")
    render_template = "organisation/theme_list.html"

    def render(self, context, instance, placeholder):
        context = super(ThemesPlugin, self)\
            .render(context, instance, placeholder)
        context['object_header'] = _("Themes")
        context['object_list'] = Theme.objects.all()
        return context

plugin_pool.register_plugin(ThemesPlugin)


class NetworkGroupFlagsPlugin(CMSPluginBase):
    model = CMSPlugin
    module = "OKF"
    name = _("Network Group Flags")
    render_template = "organisation/networkgroup_flags.html"

    def render(self, context, instance, placeholder):
        context = super(NetworkGroupFlagsPlugin, self)\
            .render(context, instance, placeholder)

        context['countries'] = NetworkGroup.objects.countries()
        return context

plugin_pool.register_plugin(NetworkGroupFlagsPlugin)


class SignupFormPlugin(CMSPluginBase):
    model = SignupForm
    module = "OKF"
    name = _("Signup Form")
    render_template = "organisation/signup_form.html"

    def render(self, context, instance, placeholder):
        context = super(SignupFormPlugin, self)\
            .render(context, instance, placeholder)

        context['title'] = instance.title
        context['description'] = instance.description
        return context

plugin_pool.register_plugin(SignupFormPlugin)
