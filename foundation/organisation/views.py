from django.views.decorators.cache import cache_page
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import get_object_or_404
from django.http import HttpResponse

from iso3166 import countries
import csv

from .models import (Board, Project, ProjectType, WorkingGroup,
                     NetworkGroup, NetworkGroupMembership)


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



class WorkingGroupListView(ListView):
    model = WorkingGroup
    template_name = 'organisation/workinggroup_list.html'

    def get_queryset(self):
        return WorkingGroup.objects.active()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_list'] = WorkingGroup.objects.active()
        context['incubator_list'] = WorkingGroup.objects.incubators()

        return context


class NetworkGroupDetailView(DetailView):
    model = NetworkGroup

    def get_object(self):
        country = self.kwargs.get('country', '')
        region = self.kwargs.get('region', '')
        return get_object_or_404(NetworkGroup,
                                 country_slug=country,
                                 region_slug=region)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # For country we want all members but only regional members for regions
        country = self.kwargs.get('country', None)
        region = self.kwargs.get('region', None)
        if region is None:
            context['regional_groups'] = NetworkGroup.objects.regions(country)
            members = NetworkGroupMembership.objects.filter(
                networkgroup__country_slug=country)
        else:
            members = NetworkGroupMembership.objects.filter(
                networkgroup__country_slug=country,
                networkgroup__region_slug=region)

        context['group_members'] = members.order_by('order', 'person__name')
        return context


@cache_page(60 * 30)
def networkgroup_csv_output(request):
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="network.csv"'

    writer = csv.writer(response)
    header_row = ['ISO3', 'Country', 'Map location',
                  'Local Groups status', 'Community Leaders', 'Website',
                  'Mailing List', 'Twitter handle', 'Facebook page']

    working_groups = []
    for group in WorkingGroup.objects.all():
        topic = 'Topic: {0}'.format(group.name)
        working_groups.append(topic)
    header_row.extend(working_groups)

    writer.writerow(header_row)

    for group in NetworkGroup.objects.all():
        if not countries.get(group.country.code, None):
            code = ''
        else:
            code = countries.get(group.country.code).alpha3
        row = [code,  # ISO3
               group.get_country_display(),  # Country
               '{region}, {country}'.format(
                   region=group.region,
                   country=group.get_country_display()
               ) if group.region else '',  # Map location
               group.get_group_type_display(),  # Local group status
               ', '.join([member.name
                          for member in group.members.all()]),  # Leaders
               group.homepage_url,  # Website
               group.mailinglist_url,
               group.twitter if group.twitter else '',
               group.facebook_url]

        # Find topics of working group
        group_working_groups = [g.name for g in group.working_groups.all()]
        for working_group in working_groups:
            if working_group[len('Topic: '):] in group_working_groups:
                row.append('Y')
            else:
                row.append('')

        writer.writerow(row)

    return response
