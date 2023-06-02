from django.contrib import admin

import reversion

from .models import FullBanner


class FullBannerAdmin(reversion.admin.VersionAdmin):
    list_display = ('title',)

admin.site.register(FullBanner, FullBannerAdmin)
