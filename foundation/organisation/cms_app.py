from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _


class UnitsAppHook(CMSApp):
    name = _("Units")
    urls = ["foundation.organisation.urls.units"]


class BoardAppHook(CMSApp):
    name = _("Board of Directors")
    urls = ["foundation.organisation.urls.board"]


class AdvisoryBoardAppHook(CMSApp):
    name = _("Advisory Board")
    urls = ["foundation.organisation.urls.advisoryboard"]

apphook_pool.register(UnitsAppHook)
apphook_pool.register(BoardAppHook)
apphook_pool.register(AdvisoryBoardAppHook)
