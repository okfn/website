from django.contrib import admin

import reversion

from .models import Newsletter


class NewsletterAdmin(reversion.admin.VersionAdmin):
    list_display = ("title",)


admin.site.register(Newsletter, NewsletterAdmin)
