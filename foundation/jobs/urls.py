from django.urls import re_path

from .views import JobListView

urlpatterns = [
    re_path(r"^$", JobListView.as_view(), name="jobs-list"),
]
