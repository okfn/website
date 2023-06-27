from django.contrib import admin

import reversion
from .forms import FullBannerForm
from .models import FullBanner


class FullBannerAdmin(reversion.admin.VersionAdmin):
    list_display = ("title",)
    form = FullBannerForm


admin.site.register(FullBanner, FullBannerAdmin)
