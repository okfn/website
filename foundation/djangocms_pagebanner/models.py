from django.db import models
from django.utils.translation import get_language

from cms.extensions import PageExtension
from cms.extensions.extension_pool import extension_pool
from cms.utils.i18n import get_language_code


class PageBannerExtension(PageExtension):
    banner_image = models.ImageField(upload_to='banners')
    background_color = models.CharField(max_length=50, default='', blank=True)
    font_color = models.CharField(max_length=50, default='', blank=True)

    def __unicode__(self):
        return self.extended_object.get_title(
            get_language_code(get_language()))

extension_pool.register(PageBannerExtension)
