from django.contrib import admin

import reversion

from .models import Quote


class QuoteAdmin(reversion.admin.VersionAdmin):
    list_display = ("text",)


admin.site.register(Quote, QuoteAdmin)
