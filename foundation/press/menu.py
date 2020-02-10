# flake8: noqa
from menus.base import NavigationNode
from menus.menu_pool import menu_pool
from django.utils.translation import ugettext_lazy as _
from cms.menu_bases import CMSAttachMenu
from .models import PressRelease, PressMention


class PressReleaseMenu(CMSAttachMenu):

    name = _("Press Releases")

    def get_nodes(self, request):
        nodes = []
        for release in PressRelease.objects.all():
            node = NavigationNode(
                release.title,
                release.get_absolute_url(),
                release.pk,
            )
            nodes.append(node)
        return nodes


menu_pool.register_menu(PressReleaseMenu)


#  class PressMentionMenu(CMSAttachMenu):

    #  name = _("Press Mentions")

    #  def get_nodes(self, request):
        #  nodes = []
        #  for mention in PressMention.objects.all():
            #  node = NavigationNode(
                #  mention.title,
                #  mention.get_absolute_url(),
                #  mention.pk,
            #  )
            #  nodes.append(node)
        #  return nodes


#  menu_pool.register_menu(PressMentionMenu)
