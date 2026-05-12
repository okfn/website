"""Smoke tests for the home page and a few critical entry points.

These run against `foundation.tests.urls`, the slim URL conf swapped in by
`foundation/test_settings.py` when `manage.py test` is invoked. That conf
mounts `cms.urls` at the root, so `/` is served by Django CMS just like in
production — but without the surrounding i18n/sitemap/sendemail patterns.

The test DB is empty, so there are no CMS Page objects. The point of these
tests is to catch regressions in routing, middleware, and template loading,
not to assert specific page content.
"""
import os
import unittest

from django.test import TestCase


SAMPLE_DATA_PATH = os.path.join(
    os.path.dirname(__file__), "fixtures", "sample_data.json"
)


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


@unittest.skipUnless(
    os.path.exists(SAMPLE_DATA_PATH),
    "sample_data.json not present — run `make fixtures-dump` to enable.",
)
class HomePageWithSampleDataTests(TestCase):
    """Tests that load a real slice of CMS data via fixtures and exercise
    the actual page-rendering pipeline. Regenerate the fixture with
    `make fixtures-dump` after changes to the prod-flavored DB."""

    fixtures = ["sample_data.json"]

    def test_home_renders_real_content(self):
        response = self.client.get("/", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn("text/html", response["Content-Type"])
        # The fixture includes the production home page; CMS should pick it
        # up by `is_home=True` and render its template.
        self.assertContains(response, "<html")
