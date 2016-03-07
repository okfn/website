from django.test import TestCase
from cms.api import add_plugin, create_page
from djangocms_picture.cms_plugins import PicturePlugin

from ..templatetags.cms_pages import placeholder_content


class PlaceholderContentTest(TestCase):

    def test_placeholder_content_concatenates_plugin_bodies(self):
        page = create_page('Test Page', 'cms_default.html', 'en')
        blurb = page.placeholders.get(slot='blurb')
        main = page.placeholders.get(slot='main')

        add_plugin(blurb, 'TextPlugin', 'en', body='Hello, ')
        add_plugin(blurb, 'TextPlugin', 'en', body='world!')
        add_plugin(main, 'TextPlugin', 'en', body='Not me, please.')

        self.assertEqual(placeholder_content(page), 'Hello, world!')

    def test_placeholder_content_ignores_plugins_without_bodies(self):
        page = create_page('Test Page', 'cms_default.html', 'en')
        blurb = page.placeholders.get(slot='blurb')

        add_plugin(blurb, PicturePlugin, 'en')

        self.assertEqual(placeholder_content(page), '')
