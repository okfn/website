from django.contrib import admin
import reversion
from .models import ContentList


class ContentListAdmin(reversion.admin.VersionAdmin):
    list_display = ("title",)


admin.site.register(ContentList, ContentListAdmin)
