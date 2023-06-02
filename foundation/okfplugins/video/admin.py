from django.contrib import admin

import reversion

from .models import Video


class VideoAdmin(reversion.admin.VersionAdmin):
    list_display = ('title',)

admin.site.register(Video, VideoAdmin)
