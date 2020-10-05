# -*- coding: utf-8 -*-
from django.test import TestCase
from django.test.client import RequestFactory

from cms.api import create_page, add_plugin
from cms.models.placeholdermodel import Placeholder
from cms.plugin_rendering import ContentRenderer
from cms.test_utils.testcases import CMSTestCase

from aldryn_video.cms_plugins import OEmbedVideoPlugin


URL = "https://www.youtube.com/watch?v=31KMjdC6DxE"


class OEmbedVideoPluginTests(TestCase):

    def setUp(self):
        self.url = URL

    def test_plugin_context(self):
        placeholder = Placeholder.objects.create(slot='test')
        model_instance = add_plugin(
            placeholder,
            OEmbedVideoPlugin,
            'en',
            url=self.url,
        )
        model_instance.clean()
        plugin_instance = model_instance.get_plugin_class_instance()
        context = plugin_instance.render({}, model_instance, None)
        self.assertIn('instance', context)

    def test_plugin_html(self):
        placeholder = Placeholder.objects.create(slot='test')
        model_instance = add_plugin(
            placeholder,
            OEmbedVideoPlugin,
            'en',
            url=self.url,
        )
        model_instance.clean()
        renderer = ContentRenderer(request=RequestFactory())
        html = renderer.render_plugin(model_instance, {})
        expected_response = (
            '<iframe src="https://www.youtube.com/embed/31KMjdC6DxE?feature=oembed"\n'
            '            class="embed-responsive-item"\n'
            '            style=""></iframe>\n'
        )
        self.assertIn(expected_response.strip(), html.strip())


class VideoTestCase(CMSTestCase):
    def setUp(self):
        self.url = URL
        self.super_user = self._create_user("test", True, True)

    def test_plugin_edit(self):
        page = create_page(title='page', template='cms_homepage.html', language='en')
        plugin = add_plugin(
            page.placeholders.get(slot='banner video'),
            OEmbedVideoPlugin,
            'en',
            url=self.url,
            auto_play=True,
            width=560,
            height=315
        )
        plugin.clean()
        plugin.save()
        page.publish('en')
        response = self.client.get(page.get_absolute_url('en'))
        expected_response = (
            '<iframe src="https://www.youtube.com/embed/31KMjdC6DxE?feature=oembed&amp;autoplay=1"\n'
            '            class="embed-responsive-item"\n'
            '            style="width: 560px; height: 315px;"></iframe>\n'
        )
        self.assertContains(response, expected_response)
