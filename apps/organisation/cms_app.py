from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _

class UnitsAppHook(CMSApp):
    name = _("Units")
    urls = ["apps.organisation.urls"]

apphook_pool.register(UnitsAppHook)
