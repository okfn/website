from django.contrib import admin

import reversion

from .models import Banner


class BannerAdmin(reversion.admin.VersionAdmin):
    list_display = ('title',)

admin.site.register(Banner, BannerAdmin)
