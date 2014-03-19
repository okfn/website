import reversion

from django.contrib import admin
from .models import (Person, Unit, Board, Theme, Project, ProjectType,
                     WorkingGroup, NetworkGroup, UnitMembership,
                     BoardMembership, NetworkGroupMembership)


class PersonAdmin(reversion.VersionAdmin):
    list_display = ('name', 'email', 'twitter')
    ordering = ('name',)

admin.site.register(Person, PersonAdmin)


class UnitMembershipInline(admin.TabularInline):
    model = UnitMembership


class UnitAdmin(reversion.VersionAdmin):
    list_display = ('name',)
    ordering = ('name',)

    inlines = [UnitMembershipInline]

admin.site.register(Unit, UnitAdmin)


class BoardMembershipInline(admin.TabularInline):
    model = BoardMembership


class BoardAdmin(reversion.VersionAdmin):
    list_display = ('name',)
    ordering = ('name',)

    prepopulated_fields = {"slug": ("name",)}
    inlines = [BoardMembershipInline]

admin.site.register(Board, BoardAdmin)


class ProjectAdmin(reversion.VersionAdmin):
    list_display = ('name',)
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(Project, ProjectAdmin)


class ProjectTypeAdmin(reversion.VersionAdmin):
    list_display = ('name',)

admin.site.register(ProjectType, ProjectTypeAdmin)


class ThemeAdmin(reversion.VersionAdmin):
    list_display = ('name',)

admin.site.register(Theme, ThemeAdmin)


class WorkingGroupAdmin(reversion.VersionAdmin):
    list_display = ('name',)

    prepopulated_fields = {"slug": ("name",)}

admin.site.register(WorkingGroup, WorkingGroupAdmin)


class NetworkGroupMembershipInline(admin.TabularInline):
    model = NetworkGroupMembership


class WorkingGroupInNetworksInline(admin.TabularInline):
    model = NetworkGroup.working_groups.through


class NetworkGroupAdmin(reversion.VersionAdmin):
    list_display = ('name', 'country',)
    ordering = ('country', 'name')
    exclude = ('country_slug', 'region_slug', 'working_groups')

    inlines = [NetworkGroupMembershipInline, WorkingGroupInNetworksInline]

admin.site.register(NetworkGroup, NetworkGroupAdmin)
