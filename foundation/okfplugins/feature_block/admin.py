from django.contrib import admin

import reversion
from .forms import FeatureBlockForm
from .models import FeatureBlock


class FeatureBlockAdmin(reversion.admin.VersionAdmin):
    list_display = ('title',)
    form = FeatureBlockForm


admin.site.register(FeatureBlock, FeatureBlockAdmin)
