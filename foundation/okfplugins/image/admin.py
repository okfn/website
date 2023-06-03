from django.contrib import admin

import reversion

from .models import OKImage


class OKImageAdmin(reversion.admin.VersionAdmin):
    list_display = ('text',)

admin.site.register(OKImage, OKImageAdmin)
