from django.views.generic.base import TemplateView


class JobListView(TemplateView):
    template_name = "jobs/job_list.html"


class JobHelperView(TemplateView):
    template_name = "jobs/job_helper.html"
