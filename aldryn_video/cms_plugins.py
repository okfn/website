# -*- coding: utf-8 -*-
from django.utils.six.moves.urllib.parse import urljoin

from django.templatetags.static import PrefixNode
from django.utils.translation import ugettext_lazy as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from aldryn_video import models


class OEmbedVideoPlugin(CMSPluginBase):

    name = _('Video')
    model = models.OEmbedVideoPlugin
    render_template = 'aldryn_video/video.html'
    text_enabled = True

    fieldsets = (
        (None,
         {'fields': ['url']},
        ),
        (_('Advanced Options'),
         {'fields': [
             ('width', 'height'),
             ('iframe_width', 'iframe_height'),
             'auto_play',
             'loop_video',
             'custom_params'
         ]}
        )
    )

    def render(self, context, instance, placeholder):
        context['instance'] = instance
        return context

    def icon_src(self, instance):
        path = 'img/aldryn_video/video-32x32.png'
        prefix = PrefixNode.handle_simple("STATIC_URL") or PrefixNode.handle_simple("MEDIA_URL")
        return urljoin(prefix, path)

plugin_pool.register_plugin(OEmbedVideoPlugin)
