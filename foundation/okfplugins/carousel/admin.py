from django.contrib import admin

import reversion

from .models import Carousel


class CarouselAdmin(reversion.admin.VersionAdmin):
    list_display = ("title",)


admin.site.register(Carousel, CarouselAdmin)
