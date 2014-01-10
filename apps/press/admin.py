from django.contrib import admin
from django.db import models

from pagedown.widgets import AdminPagedownWidget

from .models import PressRelease, PressMention


class PressReleaseAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': AdminPagedownWidget},
    }
    list_display = ('title', 'release_date', 'published')

admin.site.register(PressRelease, PressReleaseAdmin)


class PressMentionAdmin(admin.ModelAdmin):
    list_display = ('title', 'publisher', 'url')

admin.site.register(PressMention, PressMentionAdmin)
