from django.conf import settings
from django.conf.urls import include, url
from django.views.generic import TemplateView
from django.views.generic import RedirectView

from django.contrib import admin

from foundation.organisation.views import relatable_person

admin.autodiscover()

from haystack.views import SearchView
from cms.sitemaps import CMSSitemap

ARCHIVE_ROOT = 'http://webarchive.okfn.org/okfn.org/201404'

urlpatterns = [
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^robots.txt$', TemplateView.as_view(template_name="robots.txt",
                                              content_type="text/plain"),
        name="robots_file"),
    url('', include('sendemail.urls')),
]

# Allow testing of error pages in development
if settings.DEBUG:
    urlpatterns += [
        url(r'^400/$', 'django.views.defaults.bad_request'),
        url(r'^403/$', 'django.views.defaults.permission_denied'),
        url(r'^404/$', 'django.views.defaults.page_not_found'),
        url(r'^500/$', 'django.views.defaults.server_error'),
    ]

# Login/logout, password changes and resets
urlpatterns += [
    url(
        r'^login/$',
        'django.contrib.auth.views.login',
        {'template_name': 'accounts/login.html'},
        name='login'),
    url(
        r'^logout/$',
        'django.contrib.auth.views.logout',
        {'next_page': '/'},
        name='logout'
    ),
    url(
        r'^password/change/$',
        'django.contrib.auth.views.password_change',
        name='password_change'
    ),
    url(
        r'^password/change/done/$',
        'django.contrib.auth.views.password_change_done',
        name='password_change_done'
    ),
    url(
        r'^password/reset/$',
        'django.contrib.auth.views.password_reset',
        name='password_reset'
    ),
    url(
        r'^password/reset/done/$',
        'django.contrib.auth.views.password_reset_done',
        name='password_reset_done'
    ),
    url(
        r'^password/reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        'django.contrib.auth.views.password_reset_confirm',
        name='password_reset_confirm'
    ),
    url(
        r'^password/reset/complete/$',
        'django.contrib.auth.views.password_reset_complete',
        name='password_reset_complete'
    ),
]

# Search patterns (do not use haystack.url
# since we're using an older version of haystack
# because of django-cms-search)
urlpatterns += [
    url(r'^search/', SearchView(), name='haystack_search'),
]

# CMS patterns
urlpatterns += [
    url(r'^sitemap\.xml$',
        'django.contrib.sitemaps.views.sitemap',
        {'sitemaps': {'cmspages': CMSSitemap}}),
    url(r'^sitemap/$',
        TemplateView.as_view(template_name='sitemap.html')),

    # Fallthrough prefix redirects. WARNING: these will override any pages
    # created in the CMS with these names.
    url(r'^blogs/(?P<remain>.+)$',
        RedirectView.as_view(url=ARCHIVE_ROOT + '/blogs/%(remain)s',
                             permanent=True)),
    url(r'^members/(?P<remain>.+)$',
        RedirectView.as_view(url=ARCHIVE_ROOT + '/members/%(remain)s',
                             permanent=True)),
    url(r'^wp-content/(?P<remain>.+)$',
        RedirectView.as_view(url=ARCHIVE_ROOT + '/wp-content/%(remain)s',
                             permanent=True)),
    url(r'^wp-includes/(?P<remain>.+)$',
        RedirectView.as_view(url=ARCHIVE_ROOT + '/wp-includes/%(remain)s',
                             permanent=True)),

    # we would like to properly do this from within the cms
    # but it does not work with `csrf_exempt`. See
    # https://github.com/divio/django-cms/issues/4599
    url(r'^api$', relatable_person, name='relatable-person'),

    # Fallthrough for CMS managed pages
    url(r'^', include('cms.urls'))
]
