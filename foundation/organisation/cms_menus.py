from menus.base import NavigationNode
from menus.menu_pool import menu_pool
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from cms.menu_bases import CMSAttachMenu


class ProjectMenu(CMSAttachMenu):

    name = _("Projects")

    def get_nodes(self, request):
        current_projects = NavigationNode(
            'Current projects',
            reverse('projects'),
            1337,
        )
        old_projects = NavigationNode(
            'Old projects',
            reverse('projects_old'),
            1338,
        )
        nodes = [current_projects, old_projects]
        return nodes


menu_pool.register_menu(ProjectMenu)
