from django import template

from classytags.arguments import Argument
from classytags.core import Options
from classytags.helpers import AsTag

from cms.models import Page
from cms.utils import get_language_from_request, get_cms_setting, get_site_id

from cms.templatetags.cms_tags import _get_cache_key, _get_page_by_untyped_arg

register = template.Library()


class PageUrl(AsTag):
    name = 'page_url'

    options = Options(
        Argument('page_lookup'),
        Argument('lang', required=False, default=None),
        Argument('site', required=False, default=None),
        'as',
        Argument('varname', required=False, resolve=False),
    )

    # We override render_tag here so as to provide backwards-compatible
    # behaviour when varname is not provided. If varname is not provided, and
    # the specified page cannot be found, we pass through the Page.DoesNotExist
    # exception. If varname is provided, we swallow the exception and just set
    # the value to None.
    def render_tag(self, context, **kwargs):
        varname = kwargs.pop(self.varname_name)
        try:
            value = self.get_value(context, **kwargs)
        except Page.DoesNotExist:
            if not varname:
                raise
            else:
                value = ''

        if varname:
            context[varname] = value
            return ''
        return value

    def get_value(self, context, page_lookup, lang, site):
        from django.core.cache import cache
        site_id = get_site_id(site)
        request = context.get('request', False)
        if not request:
            return None

        if request.current_page == "dummy":
            return None
        if lang is None:
            lang = get_language_from_request(request)
        cache_key = _get_cache_key('page_url', page_lookup, lang, site_id) + \
            '_type:absolute_url'
        url = cache.get(cache_key)
        if not url:
            page = _get_page_by_untyped_arg(page_lookup, request, site_id)
            if page:
                url = page.get_absolute_url(language=lang)
                cache.set(cache_key, url,
                          get_cms_setting('CACHE_DURATIONS')['content'])
        if url:
            return url
        return None


register.tag(PageUrl)
register.tag('page_id_url', PageUrl)
