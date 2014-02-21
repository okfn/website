from pagedown.widgets import AdminPagedownWidget
import reversion

from django.contrib import admin
from django.db import models
from .models import Job


class JobAdmin(reversion.VersionAdmin):
    formfield_overrides = {
        models.TextField: {'widget': AdminPagedownWidget},
    }
    list_display = ('title', 'submission_closes', 'submission_email')
    # On the jobs page, the jobs nearest their deadlines should display first,
    # hence the model's default ordering of `submission_closes ASC`. But in the
    # admin, old jobs don't roll off the "top" of the page, so we actually want
    # the reverse ordering.
    ordering = ('-submission_closes',)

admin.site.register(Job, JobAdmin)
