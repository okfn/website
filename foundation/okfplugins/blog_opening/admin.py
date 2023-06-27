from django.contrib import admin

import reversion

from .models import BlogOpening


class BlogOpeningAdmin(reversion.admin.VersionAdmin):
    list_display = ("title",)


admin.site.register(BlogOpening, BlogOpeningAdmin)
