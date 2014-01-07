from django.utils import timezone
from django.views.generic.list import ListView

from .models import Job


class JobListView(ListView):
    model = Job

    def get_queryset(self):
        # Only return jobs for which the submission close time is in the
        # future.
        return Job.objects.filter(submission_closes__gt=timezone.now())
