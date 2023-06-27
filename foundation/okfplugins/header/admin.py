from django.contrib import admin
import reversion
from .forms import HeaderForm
from .models import Header


class HeaderAdmin(reversion.admin.VersionAdmin):
    list_display = ("title", "header_type")
    form = HeaderForm


admin.site.register(Header, HeaderAdmin)
