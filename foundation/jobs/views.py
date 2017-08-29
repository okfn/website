from django.views.generic.base import TemplateView
from django.views.decorators.clickjacking import xframe_options_exempt


class JobListView(TemplateView):
    template_name = "jobs/job_list.html"


class JobHelperView(TemplateView):
    template_name = "jobs/job_helper.html"

    @xframe_options_exempt
    def get(self, request, *args, **kwargs):
        return super(JobHelperView, self).get(request, *args, **kwargs)
