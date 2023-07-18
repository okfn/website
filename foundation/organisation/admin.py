import reversion

from django.contrib import admin
from .forms import (
    PersonForm, WorkingGroupForm
)
from .models import (
    Person, Unit, Board,
    WorkingGroup, NetworkGroup, UnitMembership,
    BoardMembership, NetworkGroupMembership, SideBarExtension
)

from cms.extensions import PageExtensionAdmin


class PersonAdmin(reversion.admin.VersionAdmin):
    list_display = ('name', 'email', 'twitter', 'username_on_slack')
    ordering = ('name',)
    search_fields = ('name', 'email')
    form = PersonForm


admin.site.register(Person, PersonAdmin)


class UnitMembershipInline(admin.TabularInline):
    model = UnitMembership


class UnitAdmin(reversion.admin.VersionAdmin):
    list_display = ('name',)
    ordering = ('name',)

    inlines = [UnitMembershipInline]


admin.site.register(Unit, UnitAdmin)


class BoardMembershipInline(admin.TabularInline):
    model = BoardMembership


class BoardAdmin(reversion.admin.VersionAdmin):
    list_display = ('name',)
    ordering = ('name',)

    prepopulated_fields = {"slug": ("name",)}
    inlines = [BoardMembershipInline]


admin.site.register(Board, BoardAdmin)


class WorkingGroupAdmin(reversion.admin.VersionAdmin):
    list_display = ('name',)

    prepopulated_fields = {"slug": ("name",)}
    form = WorkingGroupForm


admin.site.register(WorkingGroup, WorkingGroupAdmin)


class NetworkGroupMembershipInline(admin.TabularInline):
    model = NetworkGroupMembership


class WorkingGroupInNetworksInline(admin.TabularInline):
    model = NetworkGroup.working_groups.through


class NetworkGroupAdmin(reversion.admin.VersionAdmin):
    list_display = ('name', 'country',)
    ordering = ('country', 'name')
    exclude = ('country_slug', 'region_slug', 'working_groups')

    inlines = [NetworkGroupMembershipInline, WorkingGroupInNetworksInline]


admin.site.register(NetworkGroup, NetworkGroupAdmin)


class SideBarExtensionAdmin(PageExtensionAdmin):
    pass


admin.site.register(SideBarExtension, SideBarExtensionAdmin)
