"""Smoke tests for the home page and a few critical entry points.

These run against `foundation.tests.urls`, the slim URL conf swapped in by
`foundation/test_settings.py` when `manage.py test` is invoked. That conf
mounts `cms.urls` at the root, so `/` is served by Django CMS just like in
production — but without the surrounding i18n/sitemap/sendemail patterns.

The test DB is empty, so there are no CMS Page objects. The point of these
tests is to catch regressions in routing, middleware, and template loading,
not to assert specific page content.
"""
from django.test import TestCase


class HomePageTests(TestCase):
    def test_home_does_not_error(self):
        response = self.client.get("/")
        self.assertLess(
            response.status_code,
            500,
            f"GET / returned {response.status_code}; expected < 500",
        )

    def test_home_returns_html_when_successful(self):
        response = self.client.get("/")
        if response.status_code == 200:
            self.assertIn("text/html", response["Content-Type"])


class AdminEntryPointTests(TestCase):
    def test_admin_redirects_anonymous_user(self):
        response = self.client.get("/admin/")
        self.assertEqual(response.status_code, 302)
        self.assertIn("/admin/login/", response["Location"])

    def test_admin_login_page_renders(self):
        response = self.client.get("/admin/login/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "csrfmiddlewaretoken")
