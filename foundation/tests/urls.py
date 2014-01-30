from django.conf.urls import url, patterns, include

from django.contrib import admin

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/', lambda x: x, name='login'),
    url(r'^jobs/', include('apps.jobs.urls')),
    url(r'^about/', include('apps.organisation.urls')),
    url(r'^', include('cms.urls')),
)
