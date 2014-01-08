# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

from django.contrib.sites.models import Site

from cms.models import Page, Title
from cms.utils.conf import get_cms_setting
from cms.utils.i18n import get_language_list


def create_page(title, template, language, slug):

    site = Site.objects.get_current()

    # validate template
    assert template in [tpl[0] for tpl in get_cms_setting('TEMPLATES')]

    # validate language:
    assert language in get_language_list(site), get_cms_setting('LANGUAGES').get(site.pk)

    page = Page(
        created_by='python-api',
        changed_by='python-api',
        in_navigation=False,
        soft_root=False,
        reverse_id=slug,
        published=False,
        template=template,
        site=site,
    )
    page.insert_at(None, 'last-child')
    page.save()

    title = Title(
        language=language,
        title=title,
        slug=slug,
        page=page
    )
    title.save()

    page.publish()

    return page.reload()


class Migration(DataMigration):
    PAGES = (
        ('home', 'Home'),
        ('privacy-policy', 'Privacy policy'),
        ('ip-policy', 'IP policy'),
        ('terms-of-use', 'Terms of use'),
        ('jobs', 'Jobs'),
        ('contact', 'Contact'),
    )

    def forwards(self, orm):
        """
        The templates depend on these pages existing, and rather than requiring
        that users create them explicitly, this migration will create blank
        pages for them.
        """
        for shortname, title in self.PAGES:
            if not Page.objects.filter(reverse_id=shortname).exists():
                create_page(title, 'cms_default.html', 'en', shortname)

    def backwards(self, orm):
        raise RuntimeError("Cannot reverse this migration.")

    models = {
    }

    complete_apps = []
    symmetrical = True
