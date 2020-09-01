import json

from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.conf import settings

from iso3166 import countries
import csv

from .models import (Board, Project, ProjectType, Theme, WorkingGroup,
                     NetworkGroup, NetworkGroupMembership, Person, NowDoing)

from .utils import get_activity, fail_json, extract_ograph_title


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
    paginate_by = 15
    template_name = 'organisation/project_list.html'

    def get_queryset(self):
        # Do we want to show old projects?
        show_old = self.request.path.endswith("old")
        if show_old:
            return Project.objects.filter(old_project=True)

        return Project.objects.filter(old_project=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['themes'] = Theme.objects.all()
        context['projecttypes'] = ProjectType.objects.all()
        return context


class ThemeDetailView(DetailView):
    model = Theme

    def get_context_data(self, **kwargs):
        theme = self.kwargs.get('slug', None)
        context = super().get_context_data(**kwargs)
        context['themes'] = Theme.objects.exclude(slug=theme)
        return context


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


@csrf_exempt
def relatable_person(request):
    auth = request.META.get('HTTP_AUTHORIZATION')

    if auth != settings.HUBOT_API_KEY:
        return fail_json('Not authorized', status_code=403)

    try:
        data = json.loads(request.body)
    except ValueError:
        return fail_json('Could not decode JSON data.')

    username = data.get('username')
    if not username:
        return fail_json('You need to supply a field `username`')

    person = Person.objects.filter(username_on_slack=username).first()
    if not person:
        message = 'No person with `username_on_slack` {}'.format(username)
        return fail_json(message)

    activity = get_activity(data.get('text'))

    activities_of_this_type = person.nowdoing_set.filter(doing_type=activity)
    for old_activity in activities_of_this_type:
        old_activity.delete()

    link, title = extract_ograph_title(data.get('text', ''))
    now_doing = NowDoing(person=person,
                         doing_type=activity,
                         text=title,
                         link=link)
    now_doing.save()

    message = 'You are consuming: {}'.format(now_doing.text)
    return JsonResponse({'success': True,
                         'message': message})


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
