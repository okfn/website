from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _

class UnitsAppHook(CMSApp):
    name = _("Units")
    urls = ["apps.organisation.urls.units"]

class BoardAppHook(CMSApp):
    name = _("Board of Directors")
    urls = ["apps.organisation.urls.board"]

class AdvisoryBoardAppHook(CMSApp):
    name = _("Advisory Board")
    urls = ["apps.organisation.urls.advisoryboard"]

apphook_pool.register(UnitsAppHook)
apphook_pool.register(BoardAppHook)
apphook_pool.register(AdvisoryBoardAppHook)

