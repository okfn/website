from django.contrib import admin

import reversion

from .models import JustText


class JustTextAdmin(reversion.admin.VersionAdmin):
    list_display = ('text',)

admin.site.register(JustText, JustTextAdmin)
