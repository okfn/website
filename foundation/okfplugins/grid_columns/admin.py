from django.contrib import admin

import reversion

from .models import GridColumns


class GridColumnsAdmin(reversion.admin.VersionAdmin):
    list_display = ("title",)


admin.site.register(GridColumns, GridColumnsAdmin)
