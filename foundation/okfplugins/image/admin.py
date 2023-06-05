from django.contrib import admin

import reversion
from .headers import OKImageForm
from .models import OKImage


class OKImageAdmin(reversion.admin.VersionAdmin):
    list_display = ('text',)
    form = OKImageForm


admin.site.register(OKImage, OKImageAdmin)
