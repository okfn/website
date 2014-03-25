from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _
from .menu import ProjectMenu, ThemeMenu, NetworkGroupMenu


class UnitsAppHook(CMSApp):
    name = _("Units")
    urls = ["foundation.organisation.urls.units"]

apphook_pool.register(UnitsAppHook)


class BoardAppHook(CMSApp):
    name = _("Board of Directors")
    urls = ["foundation.organisation.urls.board"]

apphook_pool.register(BoardAppHook)


class AdvisoryBoardAppHook(CMSApp):
    name = _("Advisory Board")
    urls = ["foundation.organisation.urls.advisoryboard"]

apphook_pool.register(AdvisoryBoardAppHook)


class ProjectsAppHook(CMSApp):
    name = _("Projects")
    urls = ["foundation.organisation.urls.projects"]
    menus = [ProjectMenu]

apphook_pool.register(ProjectsAppHook)


class ThemesAppHook(CMSApp):
    name = _("Themes")
    urls = ["foundation.organisation.urls.themes"]
    menus = [ThemeMenu]

apphook_pool.register(ThemesAppHook)


class WorkingGroupsAppHook(CMSApp):
    name = _("Working Groups")
    urls = ["foundation.organisation.urls.workinggroups"]

apphook_pool.register(WorkingGroupsAppHook)


class NetworkGroupsAppHook(CMSApp):
    name = _("Network Groups")
    urls = ["foundation.organisation.urls.networkgroups"]
    menus = [NetworkGroupMenu]

apphook_pool.register(NetworkGroupsAppHook)
