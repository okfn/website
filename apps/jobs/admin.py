from django.contrib import admin
from .models import Job

class JobAdmin(admin.ModelAdmin):
    pass
admin.site.register(Job, JobAdmin)
