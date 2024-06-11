import reversion

from django.contrib import admin
from .forms import PersonForm
from .models import Person, SideBarExtension

from cms.extensions import PageExtensionAdmin


class PersonAdmin(reversion.admin.VersionAdmin):
    list_display = ('name', 'email', 'twitter', 'username_on_slack')
    ordering = ('name',)
    search_fields = ('name', 'email')
    form = PersonForm


admin.site.register(Person, PersonAdmin)


class SideBarExtensionAdmin(PageExtensionAdmin):
    pass


admin.site.register(SideBarExtension, SideBarExtensionAdmin)
