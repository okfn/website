import reversion

from django.contrib import admin
from .forms import PersonForm
from .models import (
    Person, Board, NetworkGroup,
    BoardMembership, NetworkGroupMembership, SideBarExtension
)

from cms.extensions import PageExtensionAdmin


class PersonAdmin(reversion.admin.VersionAdmin):
    list_display = ('name', 'email', 'twitter', 'username_on_slack')
    ordering = ('name',)
    search_fields = ('name', 'email')
    form = PersonForm


admin.site.register(Person, PersonAdmin)


class BoardMembershipInline(admin.TabularInline):
    model = BoardMembership


class BoardAdmin(reversion.admin.VersionAdmin):
    list_display = ('name',)
    ordering = ('name',)

    prepopulated_fields = {"slug": ("name",)}
    inlines = [BoardMembershipInline]


admin.site.register(Board, BoardAdmin)


class NetworkGroupMembershipInline(admin.TabularInline):
    model = NetworkGroupMembership


class NetworkGroupAdmin(reversion.admin.VersionAdmin):
    list_display = ('name', 'country',)
    ordering = ('country', 'name')
    exclude = ('country_slug', 'region_slug')

    inlines = [NetworkGroupMembershipInline]


admin.site.register(NetworkGroup, NetworkGroupAdmin)


class SideBarExtensionAdmin(PageExtensionAdmin):
    pass


admin.site.register(SideBarExtension, SideBarExtensionAdmin)
