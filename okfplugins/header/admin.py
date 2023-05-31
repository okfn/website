from django.contrib import admin

import reversion

from .models import Header


class HeaderAdmin(reversion.admin.VersionAdmin):
    list_display = ('title',)

admin.site.register(Header, HeaderAdmin)
