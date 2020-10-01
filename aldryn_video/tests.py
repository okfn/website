# -*- coding: utf-8 -*-
from django.test import TestCase
from cms.api import create_page, add_plugin
from cms.test_utils.testcases import (CMSTestCase, URL_CMS_PLUGIN_EDIT)
from aldryn_video.cms_plugins import OEmbedVideoPlugin
from cms.models.placeholdermodel import Placeholder
from django.utils.safestring import SafeText

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
        html = model_instance.render_plugin({})
        expected_response = ('<iframe src="https://www.youtube.com/embed/31KMjdC6DxE?feature=oembed"\n'
            '    class="iframe iframe-video"\n'
            '    style=""></iframe>\n')
        self.assertEqual(html.strip(), expected_response.strip())


class VideoTestCase(CMSTestCase):
    def setUp(self):
        self.url = URL
        self.super_user = self._create_user("test", True, True)

    def test_plugin_edit(self):
        page = create_page(title='page',template='page.html',language='en')
        plugin = add_plugin(
            page.placeholders.get(slot='content'),
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
        expected_response = ('<iframe src="https://www.youtube.com/embed/31KMjdC6DxE?feature=oembed&amp;autoplay=1"\n'
            '    class="iframe iframe-video"\n'
            '    style="width: 560px; height: 315px;"></iframe>\n')
        self.assertContains(response, expected_response)
