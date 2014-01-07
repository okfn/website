from pagedown.widgets import AdminPagedownWidget

from django.contrib import admin
from django.db import models
from .models import Job


class JobAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': AdminPagedownWidget},
    }
admin.site.register(Job, JobAdmin)
