from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import gettext_lazy as _
from .cms_menus import ProjectMenu


class UnitsAppHook(CMSApp):
    name = _("Units")

    def get_urls(self, page=None, language=None, **kwargs):
        return ["foundation.organisation.urls.units"]


apphook_pool.register(UnitsAppHook)


class BoardAppHook(CMSApp):
    name = _("Board of Directors")

    def get_urls(self, page=None, language=None, **kwargs):
        return ["foundation.organisation.urls.board"]


apphook_pool.register(BoardAppHook)


class AdvisoryBoardAppHook(CMSApp):
    name = _("Advisory Board")

    def get_urls(self, page=None, language=None, **kwargs):
        return ["foundation.organisation.urls.advisoryboard"]


apphook_pool.register(AdvisoryBoardAppHook)


class ProjectsAppHook(CMSApp):
    name = _("Projects")

    def get_menus(self, page=None, language=None, **kwargs):
        return [ProjectMenu]

    def get_urls(self, page=None, language=None, **kwargs):
        return ["foundation.organisation.urls.projects"]


apphook_pool.register(ProjectsAppHook)


class WorkingGroupsAppHook(CMSApp):
    name = _("Working Groups")

    def get_urls(self, page=None, language=None, **kwargs):
        return ["foundation.organisation.urls.workinggroups"]


apphook_pool.register(WorkingGroupsAppHook)


class NetworkGroupsAppHook(CMSApp):
    name = _("Network Groups")

    def get_urls(self, page=None, language=None, **kwargs):
        return ["foundation.organisation.urls.networkgroups"]


apphook_pool.register(NetworkGroupsAppHook)
