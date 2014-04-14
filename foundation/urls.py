from django.conf import settings
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.views.generic import RedirectView

from django.contrib import admin
admin.autodiscover()

from haystack.views import SearchView
from cms.sitemaps import CMSSitemap

ARCHIVE_ROOT = 'http://webarchive.okfn.org/okfn.org/201404'

urlpatterns = patterns(
    '',
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    )

# Allow testing of error pages in development
if settings.DEBUG:
    urlpatterns += patterns(
        '',
        (r'^400/$', 'django.views.defaults.bad_request'),
        (r'^403/$', 'django.views.defaults.permission_denied'),
        (r'^404/$', 'django.views.defaults.page_not_found'),
        (r'^500/$', 'django.views.defaults.server_error'),
        )

# Login/logout, password changes and resets
urlpatterns += patterns(
    'django.contrib.auth.views',
    url(r'^login/$', 'login',
        {'template_name': 'accounts/login.html'},
        name='login'),
    url(r'^logout/$', 'logout', {'next_page': '/'}, name='logout'),
    url(r'^password/change/$', 'password_change',
        name='password_change'),
    url(r'^password/change/done/$', 'password_change_done',
        name='password_change_done'),
    url(r'^password/reset/$', 'password_reset',
        name='password_reset'),
    url(r'^password/reset/done/$', 'password_reset_done',
        name='password_reset_done'),
    url(r'^password/reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        'password_reset_confirm',
        name='password_reset_confirm'),
    url(r'^password/reset/complete/$',
        'password_reset_complete',
        name='password_reset_complete'),
    )

# Search patterns (do not use haystack.url
# since we're using an older version of haystack
# because of django-cms-search)
urlpatterns += patterns(
    'haystack.views',
    url(r'^search/', SearchView(), name='haystack_search'),
    )

# CMS patterns
urlpatterns += patterns(
    '',
    url(r'^sitemap\.xml$',
        'django.contrib.sitemaps.views.sitemap',
        {'sitemaps': {'cmspages': CMSSitemap}}),
    url(r'^sitemap/$',
        TemplateView.as_view(template_name='sitemap.html')),

    # Fallthrough prefix redirects. WARNING: these will override any pages
    # created in the CMS with these names.
    url(r'^blogs/(?P<remain>.+)$',
        RedirectView.as_view(url=ARCHIVE_ROOT + '/blogs/%(remain)s')),
    url(r'^members/(?P<remain>.+)$',
        RedirectView.as_view(url=ARCHIVE_ROOT + '/members/%(remain)s')),
    url(r'^wp-content/(?P<remain>.+)$',
        RedirectView.as_view(url=ARCHIVE_ROOT + '/wp-content/%(remain)s')),
    url(r'^wp-includes/(?P<remain>.+)$',
        RedirectView.as_view(url=ARCHIVE_ROOT + '/wp-includes/%(remain)s')),

    # Fallthrough for CMS managed pages
    url(r'^', include('cms.urls'))
    )
