# -*- coding: utf-8 -*-
from django.utils.six.moves.urllib.parse import urlencode
from django.utils.six.moves.urllib.parse import parse_qs, urlparse, urlunparse

from bs4 import BeautifulSoup

import micawber
from micawber.exceptions import ProviderNotFoundException, ProviderException

providers = micawber.bootstrap_basic()


default_cms_plugin_table_mapping = (
    # (old_name, new_name),
    ('cmsplugin_oembedvideoplugin', 'aldryn_video_oembedvideoplugin'),
)


def build_html_iframe(response, url_params=None, iframe_attrs=None):
    html = response.get('html', '')

    if url_params is None:
        url_params = {}

    if iframe_attrs is None:
        iframe_attrs = {}

    if html:
        # What follows is a pretty nasty looking "hack"
        # oEmbed hss not implemented some parameters
        # and so for these we need to add them manually to the iframe.
        html = BeautifulSoup(html).iframe

        data_url = response.get('player_url', html['src'])
        player_url = urlparse(data_url)

        queries = parse_qs(player_url.query)
        url_params.update(queries)

        url_parts = list(player_url)
        url_parts[4] = urlencode(url_params, True)

        html['src'] = urlunparse(url_parts)

        for key, value in iframe_attrs.iteritems():
            if value:
                html[key] = value
    return unicode(html)


def get_player_url(response):
    html = BeautifulSoup(markup=response.get('html', ''))
    if html.iframe:
        return html.iframe.attrs['src']
    return None


def get_embed_code(**kwargs):
    try:
        data = providers.request(**kwargs)
    except (ProviderNotFoundException, ProviderException) as e:
        raise Exception(e.message)
    else:
        return data

def rename_tables(db, table_mapping=None, reverse=False):
    """
    renames tables from source to destination name, if the source exists and the
    destination does not exist yet.
    taken from cmsplugin-filer:cmsplugin_filer_utils.migration
    (thanks to @stefanfoulis)
    """
    from django.db import connection

    if not table_mapping:
        table_mapping = default_cms_plugin_table_mapping

    if reverse:
        table_mapping = [(dst, src) for src, dst in table_mapping]
    table_names = connection.introspection.table_names()
    for source, destination in table_mapping:
        if source in table_names and destination in table_names:
            print("    WARNING: not renaming {0} to {1}, because both tables "
                  "already exist.".format(source, destination))
        elif source in table_names and destination not in table_names:
            print("     - renaming {0} to {1}".format(source, destination))
            db.rename_table(source, destination)


def rename_tables_old_to_new(db, table_mapping=None):
    return rename_tables(db, table_mapping, reverse=False)


def rename_tables_new_to_old(db, table_mapping=None):
    return rename_tables(db, table_mapping, reverse=True)