from django.contrib import admin
from .models import SideBarExtension

from cms.extensions import PageExtensionAdmin


class SideBarExtensionAdmin(PageExtensionAdmin):
    pass


admin.site.register(SideBarExtension, SideBarExtensionAdmin)
