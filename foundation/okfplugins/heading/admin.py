from django.contrib import admin

import reversion

from .models import Heading


class HeadingAdmin(reversion.admin.VersionAdmin):
    list_display = ('title',)

admin.site.register(Heading, HeadingAdmin)
