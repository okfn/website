from menus.base import NavigationNode
from menus.menu_pool import menu_pool
from django.utils.translation import ugettext_lazy as _
from cms.menu_bases import CMSAttachMenu
from .models import Project


class ProjectMenu(CMSAttachMenu):

    name = _("Projects")

    def get_nodes(self, request):
        nodes = []
        for project in Project.objects.all():
            node = NavigationNode(
                project.name,
                project.get_absolute_url(),
                project.pk,
            )
            nodes.append(node)
        return nodes

menu_pool.register_menu(ProjectMenu)
