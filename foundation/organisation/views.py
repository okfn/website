from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import get_object_or_404

from .models import Board, Project, WorkingGroup


class BoardView(DetailView):
    model = Board
    template_name = 'organisation/board_details.html'
    board = None

    def get_object(self, *args, **kwargs):
        # Try to find the board based on the slug or 404
        return get_object_or_404(Board, slug=self.board)


class ProjectDetailView(DetailView):
    model = Project
    template_name = 'organisation/project_detail.html'


class ProjectListView(ListView):
    model = Project
    paginate_by = 10
    template_name = 'organisation/project_list.html'


class WorkingGroupListView(ListView):
    model = WorkingGroup

    def get_queryset(self):
        return WorkingGroup.objects.active()

    def get_context_data(self, **kwargs):
        context = super(WorkingGroupListView, self).get_context_data(**kwargs)
        context['incubator_list'] = WorkingGroup.objects.incubators()

        return context
