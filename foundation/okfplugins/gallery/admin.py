from django.contrib import admin

import reversion

from .models import Gallery


class GalleryAdmin(reversion.admin.VersionAdmin):
    list_display = ('title',)

admin.site.register(Gallery, GalleryAdmin)
