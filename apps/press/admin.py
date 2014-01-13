from django.contrib import admin
from django.db import models

from pagedown.widgets import AdminPagedownWidget
import reversion

from .models import PressRelease, PressMention


class PressReleaseAdmin(reversion.VersionAdmin):
    formfield_overrides = {
        models.TextField: {'widget': AdminPagedownWidget},
    }
    list_display = ('title', 'release_date', 'published')

admin.site.register(PressRelease, PressReleaseAdmin)


class PressMentionAdmin(reversion.VersionAdmin):
    list_display = ('title', 'publisher', 'url')

admin.site.register(PressMention, PressMentionAdmin)
