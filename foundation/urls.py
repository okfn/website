from django.conf import settings
from django.urls import include, re_path
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.views.generic import RedirectView
from django.contrib.auth import views as admin_views
from django.views import defaults as default_views

from django.contrib import admin
from django.contrib.sitemaps.views import sitemap

from cms.sitemaps import CMSSitemap

admin.autodiscover()

ARCHIVE_ROOT = "http://webarchive.okfn.org/okfn.org/201404"

urlpatterns = [
    re_path(r"^admin/doc/", include("django.contrib.admindocs.urls")),
    re_path(r"^admin/", admin.site.urls),
    re_path(
        r"^robots.txt$",
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
        name="robots_file",
    ),
    re_path("", include("sendemail.urls")),
]

# Allow testing of error pages in development
if settings.DEBUG:
    urlpatterns += [
        re_path(r"^400/$", default_views.bad_request),
        re_path(r"^403/$", default_views.permission_denied),
        re_path(r"^404/$", default_views.page_not_found),
        re_path(r"^500/$", default_views.server_error),
    ]

# Login/logout, password changes and resets
urlpatterns += [
    re_path(
        r"^login/$",
        admin_views.LoginView.as_view(),
        {"template_name": "accounts/login.html"},
        name="login",
    ),
    re_path(
        r"^logout/$",
        admin_views.LogoutView.as_view(),
        {"next_page": "/"},
        name="logout",
    ),
    re_path(
        r"^password/change/$",
        admin_views.PasswordChangeView.as_view(),
        name="password_change",
    ),
    re_path(
        r"^password/change/done/$",
        admin_views.PasswordChangeDoneView.as_view(),
        name="password_change_done",
    ),
    re_path(
        r"^password/reset/$",
        admin_views.PasswordResetView.as_view(),
        name="password_reset",
    ),
    re_path(
        r"^password/reset/done/$",
        admin_views.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    re_path(
        r"^password/reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$",
        admin_views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    re_path(
        r"^password/reset/complete/$",
        admin_views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
]

urlpatterns += [
    re_path(r"^'search/", include("haystack.urls")),
]

# CMS patterns
urlpatterns += [
    re_path(r"^sitemap\.xml$", sitemap, {"sitemaps": {"cmspages": CMSSitemap}}),
    re_path(r"^sitemap/$", TemplateView.as_view(template_name="sitemap.html")),
    # Fallthrough prefix redirects. WARNING: these will override any pages
    # created in the CMS with these names.
    re_path(
        r"^blogs/(?P<remain>.+)$",
        RedirectView.as_view(url=ARCHIVE_ROOT + "/blogs/%(remain)s", permanent=True),
    ),
    re_path(
        r"^members/(?P<remain>.+)$",
        RedirectView.as_view(url=ARCHIVE_ROOT + "/members/%(remain)s", permanent=True),
    ),
    re_path(
        r"^wp-content/(?P<remain>.+)$",
        RedirectView.as_view(
            url=ARCHIVE_ROOT + "/wp-content/%(remain)s", permanent=True
        ),
    ),
    re_path(
        r"^wp-includes/(?P<remain>.+)$",
        RedirectView.as_view(
            url=ARCHIVE_ROOT + "/wp-includes/%(remain)s", permanent=True
        ),
    ),
    # Fallthrough for CMS managed pages
    re_path(r"^", include("cms.urls")),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
