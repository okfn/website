from django.contrib import admin
from django import forms
import reversion
from .models import FooterModel


class FooterAdmin(reversion.admin.VersionAdmin):
    list_display = ("title",)


admin.site.register(FooterModel, FooterAdmin)
