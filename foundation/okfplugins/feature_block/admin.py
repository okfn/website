from django.contrib import admin

import reversion

from .models import FeatureBlock


class FeatureBlockAdmin(reversion.admin.VersionAdmin):
    list_display = ('title',)

admin.site.register(FeatureBlock, FeatureBlockAdmin)
