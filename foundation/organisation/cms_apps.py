from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import gettext_lazy as _


class NetworkGroupsAppHook(CMSApp):
    name = _("Network Groups")

    def get_urls(self, page=None, language=None, **kwargs):
        return ["foundation.organisation.urls.networkgroups"]


apphook_pool.register(NetworkGroupsAppHook)
