from cms.api import get_page_draft
from cms.toolbar_pool import toolbar_pool
from cms.toolbar_base import CMSToolbar
from cms.utils import get_cms_setting
from cms.utils.permissions import has_page_change_permission
from django.core.urlresolvers import reverse, NoReverseMatch
from django.utils.translation import ugettext_lazy as _
from .models import PageBannerExtension


@toolbar_pool.register
class PageBannerExtensionToolbar(CMSToolbar):
    def populate(self):
        # always use draft if we have a page
        self.page = get_page_draft(self.request.current_page)

        if not self.page:
            # Nothing to do
            return

        # check global permissions if CMS_PERMISSIONS is active
        if get_cms_setting('PERMISSION'):
            has_global_current_page_change_permission = \
                has_page_change_permission(self.request)
        else:
            has_global_current_page_change_permission = False
            # check if user has page edit permission
        can_change = (self.request.current_page and
                      self.request.current_page.has_change_permission(
                          self.request))

        if has_global_current_page_change_permission or can_change:
            try:
                page_banner_extension = PageBannerExtension.objects.get(
                    extended_object_id=self.page.id)
            except PageBannerExtension.DoesNotExist:
                page_banner_extension = None
            try:
                if page_banner_extension:
                    url = reverse(
                        'admin:djangocms_pagebanner_pagebannerextension_change',
                        args=(page_banner_extension.pk,))
                else:
                    url = (reverse('admin:djangocms_pagebanner_pagebannerextension_add') +
                           '?extended_object=%s' % self.page.pk)
            except NoReverseMatch:
                # not in urls
                pass
            else:
                not_edit_mode = not self.toolbar.edit_mode
                current_page_menu = self.toolbar.get_or_create_menu('page')
                current_page_menu.add_modal_item(_('Page banner'),
                                                 url=url,
                                                 disabled=not_edit_mode)
