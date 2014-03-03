from django.test import TestCase
from cms.api import add_plugin, create_page
from cms.models import Page, Placeholder

from ..templatetags.cms_pages import placeholder_content


class PlaceholderContentTest(TestCase):

    def setUp(self):  # flake8: noqa
        self.page = create_page('Test Page',
                                'cms_default.html',
                                'en')
        self.blurb = self.page.placeholders.get(slot='blurb')
        self.main = self.page.placeholders.get(slot='main')

        add_plugin(self.blurb, 'TextPlugin', 'en', body='Hello, ')
        add_plugin(self.blurb, 'TextPlugin', 'en', body='world!')
        add_plugin(self.main, 'TextPlugin', 'en', body='Not me, please.')

    def test_placeholder_content_concatenates_plugin_bodies(self):
        self.assertEqual(placeholder_content(self.page), 'Hello, world!')
