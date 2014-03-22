from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _

from .menu import PressReleaseMenu, PressMentionMenu


class PressReleaseAppHook(CMSApp):
    name = _("Press Releases")
    urls = ["foundation.press.urls.pressreleases"]
    menus = [PressReleaseMenu]

apphook_pool.register(PressReleaseAppHook)


class PressMentionAppHook(CMSApp):
    name = _("Press Mentions")
    urls = ["foundation.press.urls.pressmentions"]
    menus = [PressMentionMenu]

apphook_pool.register(PressMentionAppHook)
