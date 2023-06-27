from django.contrib import admin

import reversion

from .models import HeroPunch


class HeroPunchAdmin(reversion.admin.VersionAdmin):
    list_display = ('title',)

admin.site.register(HeroPunch, HeroPunchAdmin)
