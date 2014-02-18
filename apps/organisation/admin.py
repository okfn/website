import reversion

from django.contrib import admin
from .models import Person, Unit, Board
from .models import UnitMembership, BoardMembership


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
