from django.urls import re_path, include

from django.contrib import admin

urlpatterns = [
    re_path(r"^admin/", admin.site.urls),
    re_path(r"^login/", lambda x: x, name="login"),
    re_path(r"^search/", include("haystack.urls")),
    re_path(r"^jobs/", include("foundation.jobs.urls")),
    re_path(r"^about/team", include("foundation.organisation.urls.units")),
    re_path(r"^about/board", include("foundation.organisation.urls.board")),
    re_path(
        r"^about/advisory-board", include("foundation.organisation.urls.advisoryboard")
    ),
    re_path(r"^network/", include("foundation.organisation.urls.networkgroups")),
    re_path(r"^", include("cms.urls")),
]
