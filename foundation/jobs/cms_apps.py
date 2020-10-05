from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _


class JobsAppHook(CMSApp):
    name = _("Jobs")

    def get_urls(self, page=None, language=None, **kwargs):
        return ["foundation.jobs.urls"]


apphook_pool.register(JobsAppHook)
