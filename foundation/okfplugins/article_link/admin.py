from django.contrib import admin
import reversion
from .forms import ArticleLinkForm
from .models import ArticleLink


class ArticleLinkAdmin(reversion.admin.VersionAdmin):
    list_display = ("title",)
    form = ArticleLinkForm


admin.site.register(ArticleLink, ArticleLinkAdmin)
