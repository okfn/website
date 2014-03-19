from django.db import models

from cms.extensions import PageExtension
from cms.extensions.extension_pool import extension_pool


class PageBannerExtension(PageExtension):
    banner_image = models.ImageField(upload_to='banners')
    background_color = models.CharField(max_length=50, default='', blank=True)
    font_color = models.CharField(max_length=50, default='', blank=True)

extension_pool.register(PageBannerExtension)
