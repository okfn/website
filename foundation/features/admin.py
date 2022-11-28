from django.contrib import admin

import reversion

from .models import Feature


class FeatureAdmin(reversion.admin.VersionAdmin):
    list_display = ('title', 'order', 'published')


admin.site.register(Feature, FeatureAdmin)
