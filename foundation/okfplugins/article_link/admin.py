from django.contrib import admin

import reversion

from .models import ArticleLink


class ArticleLinkAdmin(reversion.admin.VersionAdmin):
    list_display = ('title',)

admin.site.register(ArticleLink, ArticleLinkAdmin)
