from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _


class PressAppHook(CMSApp):
    name = _("Press")
    urls = ["foundation.press.urls"]

apphook_pool.register(PressAppHook)
