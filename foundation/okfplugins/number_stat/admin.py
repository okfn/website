from django.contrib import admin
import reversion
from .models import NumberStat


class NumberStatAdmin(reversion.admin.VersionAdmin):
    list_display = ("title",)


admin.site.register(NumberStat, NumberStatAdmin)
