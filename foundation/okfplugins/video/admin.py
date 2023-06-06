from django.contrib import admin

import reversion
from .forms import VideoForm
from .models import Video


class VideoAdmin(reversion.admin.VersionAdmin):
    list_display = ('title',)
    form = VideoForm


admin.site.register(Video, VideoAdmin)
