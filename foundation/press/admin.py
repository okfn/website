from django.contrib import admin
from django.db import models

from pagedown.widgets import AdminPagedownWidget
import reversion

from .models import PressRelease, PressMention


class PressReleaseAdmin(reversion.admin.VersionAdmin):
    formfield_overrides = {
        models.TextField: {'widget': AdminPagedownWidget},
    }
    list_display = ('title', 'release_date')
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(PressRelease, PressReleaseAdmin)


class PressMentionAdmin(reversion.admin.VersionAdmin):
    list_display = ('title', 'publisher', 'url')
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(PressMention, PressMentionAdmin)
