from django.conf.urls import url, patterns, include

from django.contrib import admin

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/', lambda x: x, name='login'),
    url(r'^search/', include('haystack.urls')),
    url(r'^jobs/', include('foundation.jobs.urls')),
    url(r'^press/releases', include('foundation.press.urls.pressreleases')),
    url(r'^press/mentions', include('foundation.press.urls.pressmentions')),
    url(r'^about/team', include('foundation.organisation.urls.units')),
    url(r'^about/board', include('foundation.organisation.urls.board')),
    url(r'^about/advisory-board',
        include('foundation.organisation.urls.advisoryboard')),
    url(r'^projects/', include('foundation.organisation.urls.projects')),
    url(r'^themes/', include('foundation.organisation.urls.themes')),
    url(r'^get-involved/working-groups',
        include('foundation.organisation.urls.workinggroups')),
    url(r'^network/', include('foundation.organisation.urls.networkgroups')),
    url(r'^', include('cms.urls')),
    )
