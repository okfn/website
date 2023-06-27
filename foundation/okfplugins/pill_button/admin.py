from django.contrib import admin

import reversion

from .models import PillButton


class PillButtonAdmin(reversion.admin.VersionAdmin):
    list_display = ("text",)


admin.site.register(PillButton, PillButtonAdmin)
