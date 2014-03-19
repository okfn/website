from django.contrib import admin
from .models import PageBannerExtension

from cms.extensions import PageExtensionAdmin


class PageBannerExtensionAdmin(PageExtensionAdmin):
    pass

admin.site.register(PageBannerExtension, PageBannerExtensionAdmin)
