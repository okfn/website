from django.contrib import admin

import reversion

from .models import PillsMenu


class PillsMenuAdmin(reversion.admin.VersionAdmin):
    list_display = ("title",)


admin.site.register(PillsMenu, PillsMenuAdmin)
