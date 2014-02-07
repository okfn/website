from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _


class JobsAppHook(CMSApp):
    name = _("Jobs")
    urls = ["apps.jobs.urls"]

apphook_pool.register(JobsAppHook)
