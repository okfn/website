from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.views.generic import RedirectView
from django.contrib.auth import views as admin_views
from django.views import defaults as default_views

from django.contrib import admin
from django.contrib.sitemaps.views import sitemap

from foundation.organisation.views import relatable_person

from haystack.views import SearchView
from cms.sitemaps import CMSSitemap

admin.autodiscover()

ARCHIVE_ROOT = 'http://webarchive.okfn.org/okfn.org/201404'

urlpatterns = [
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^robots.txt$', TemplateView.as_view(template_name="robots.txt",
                                              content_type="text/plain"),
        name="robots_file"),
    url('', include('sendemail.urls')),
]

# Allow testing of error pages in development
if settings.DEBUG:
    urlpatterns += [
        url(r'^400/$', default_views.bad_request),
        url(r'^403/$', default_views.permission_denied),
        url(r'^404/$', default_views.page_not_found),
        url(r'^500/$', default_views.server_error),
    ]

# Login/logout, password changes and resets
urlpatterns += [
    url(
        r'^login/$',
        admin_views.LoginView.as_view(),
        {'template_name': 'accounts/login.html'},
        name='login'),
    url(
        r'^logout/$',
        admin_views.LogoutView.as_view(),
        {'next_page': '/'},
        name='logout'
    ),
    url(
        r'^password/change/$',
        admin_views.PasswordChangeView.as_view(),
        name='password_change'
    ),
    url(
        r'^password/change/done/$',
        admin_views.PasswordChangeDoneView.as_view(),
        name='password_change_done'
    ),
    url(
        r'^password/reset/$',
        admin_views.PasswordResetView.as_view(),
        name='password_reset'
    ),
    url(
        r'^password/reset/done/$',
        admin_views.PasswordResetDoneView.as_view(),
        name='password_reset_done'
    ),
    url(
        r'^password/reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        admin_views.PasswordResetConfirmView.as_view(),
        name='password_reset_confirm'
    ),
    url(
        r'^password/reset/complete/$',
        admin_views.PasswordResetCompleteView.as_view(),
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
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': {'cmspages': CMSSitemap}}),
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


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
