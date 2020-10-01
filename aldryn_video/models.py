# -*- coding: utf-8 -*-
import re
from django.utils.six.moves.urllib.parse import urlparse

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _

from cms.models.pluginmodel import CMSPlugin

from jsonfield import JSONField

from .utils import build_html_iframe, get_embed_code, get_player_url

from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class OEmbedVideoPlugin(CMSPlugin):
    # exact provide name from youtube oembed response
    YOUTUBE = 'YouTube'

    ALLOWED_MEDIA_TYPES = ['video']

    url = models.URLField(_('URL'), max_length=100, help_text=_('vimeo and youtube supported.'))
    width = models.IntegerField(_('Width'), null=True, blank=True)
    height = models.IntegerField(_('Height'), null=True, blank=True)
    iframe_width = models.CharField(_('iframe width'), max_length=15, blank=True)
    iframe_height = models.CharField(_('iframe height'), max_length=15, blank=True)
    auto_play = models.BooleanField(_('auto play'), default=False)
    loop_video = models.BooleanField(_('loop'), help_text=_('when true, the video repeats itself when over.'), default=False)
    # cached oembed data
    oembed_data = JSONField(null=True)
    custom_params = models.CharField(_('custom params'), help_text=_('define custom params (e.g. "start=10&end=50")'), max_length=200, blank=True)

    def __str__(self):
        return self.url

    def get_oembed_params(self):
        extra = {}

        if self.width:
            extra['maxwidth'] = self.width
        if self.height:
            extra['maxheight'] = self.height
        if self.auto_play:
            extra['autoplay'] = 1
        if self.loop_video:
            extra['loop'] = 1
        if self.custom_params:
            for param in self.custom_params.split("&"):
                key, value = param.split("=")
                extra[key] = value
        return extra

    @property
    def html(self):
        if not hasattr(self, '_html'):
            params = self.get_oembed_params()
            attrs = {
                'width': self.iframe_width,
                'height': self.iframe_height
            }
            provider_name = self.oembed_data.get('provider_name', '')
            video_url = get_player_url(self.oembed_data)

            if video_url and provider_name == self.YOUTUBE and self.loop_video:
                # Unfortunately youtube requires a "playlist" parameter when using loop
                # I don't set this in get_oembed_params because it's not really an oembed thing.
                # very specific to youtube.
                url = urlparse(video_url)
                # We assume that youtube's embed format is consistent
                # and looks like http://www.youtube.com/embed/-UUx10KOWIE?feature=oembed
                params['playlist'] = url.path.split('/')[2]

            html = build_html_iframe(
                self.oembed_data,
                url_params=params,
                iframe_attrs=attrs
            )

            self._html = re.sub('(https?://)', '//', html)
        return self._html

    def clean(self):
        params = self.get_oembed_params()

        if self.url.startswith('https'):
            # scheme usually only affects youtube
            # but we don't know the provider at this point.
            # also I add this here because if added to get_oembed_params
            # the parameter stays when requesting the video.
            params['scheme'] = 'https'

        try:
            data = get_embed_code(url=self.url, **params)
        except Exception as e:
            try:
                msg = e.message
            except AttributeError:
                msg = e.args[0]
            raise ValidationError(msg)
        else:
            media_type = data.get('type')
            if media_type not in self.ALLOWED_MEDIA_TYPES:
                raise ValidationError('This must be an url for a video. The "%(type)s" type is not supported.' % dict(type=media_type))

        player_url = get_player_url(data)

        if player_url:
            data['player_url'] = player_url

        self.oembed_data = data
