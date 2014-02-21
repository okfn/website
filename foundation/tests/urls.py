from django.conf.urls import url, patterns, include

from django.contrib import admin

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/', lambda x: x, name='login'),
    url(r'^search/', include('haystack.urls')),
    url(r'^jobs/', include('foundation.jobs.urls')),
    url(r'^about/team', include('foundation.organisation.urls.units')),
    url(r'^about/board', include('foundation.organisation.urls.board')),
    url(r'^about/advisory-board',
        include('foundation.organisation.urls.advisoryboard')),
    url(r'^', include('cms.urls')),
    )
