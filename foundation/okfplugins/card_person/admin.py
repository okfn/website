from django.contrib import admin

import reversion

from .models import CardPerson


class CardPersonAdmin(reversion.admin.VersionAdmin):
    list_display = ("name", "role", "email")


admin.site.register(CardPerson, CardPersonAdmin)
