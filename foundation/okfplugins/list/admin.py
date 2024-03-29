from django.contrib import admin

import reversion

from .models import List


class ListAdmin(reversion.admin.VersionAdmin):
    list_display = ("title",)


admin.site.register(List, ListAdmin)
