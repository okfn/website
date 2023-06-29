from django.contrib import admin

import reversion

from .models import Spotlight


class SpotlightAdmin(reversion.admin.VersionAdmin):
    list_display = ("title",)


admin.site.register(Spotlight, SpotlightAdmin)
