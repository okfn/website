import collections

from cms.test_utils.testcases import CMSTestCase

from ..models import Project, ProjectType, Theme
from ..models import FeaturedProject, ProjectList
from ..cms_plugins import FeaturedProjectPlugin, ProjectListPlugin


class FeaturedProjectPluginTest(CMSTestCase):

    def setUp(self):  # flake8: noqa
        super(FeaturedProjectPluginTest, self).setUp()

        self.project = Project.objects.create(name='Project X',
            description="I could tell you, but then I'd have to kill you.")
        self.featured = FeaturedProject.objects.create(project=self.project)

    def test_adds_project_to_context(self):
        plug = FeaturedProjectPlugin()
        result = plug.render({}, self.featured, 'foo')

        self.assertEqual(self.project, result['project'])


class ProjectListPluginTest(CMSTestCase):

    def setUp(self):  # flake8: noqa
        super(ProjectListPluginTest, self).setUp()

        self.cheese = Theme.objects.create(name='Cheese')
        self.programming = ProjectType.objects.create(name='Programming')

        self.x = Project.objects.create(name='Project X', slug='project-x',
            description="I could tell you, but then I'd have to kill you.")
        self.y = Project.objects.create(name='Project Y', slug='project-y',
            description="Why, why, why?")
        self.z = Project.objects.create(name='Project Z', slug='project-z',
            description="I do believe it. I do believe it's true.")

        self.y.themes.add(self.cheese)
        self.y.save()

        self.z.themes.add(self.cheese)
        self.z.types.add(self.programming)
        self.z.save()

        self.plug = ProjectListPlugin()

    def test_all_projects_in_context_by_default(self):
        instance = ProjectList()
        result = self.plug.render({}, instance, 'foo')

        self.assertIn(self.x, result['projects'])
        self.assertIn(self.y, result['projects'])

    def test_filter_by_theme(self):
        instance = ProjectList(theme=self.cheese)
        result = self.plug.render({}, instance, 'foo')

        self.assertNotIn(self.x, result['projects'])
        self.assertIn(self.y, result['projects'])
        self.assertIn(self.z, result['projects'])

    def test_filter_by_type(self):
        instance = ProjectList(theme=self.cheese,
                               project_type=self.programming)
        result = self.plug.render({}, instance, 'foo')

        self.assertNotIn(self.x, result['projects'])
        self.assertNotIn(self.y, result['projects'])
        self.assertIn(self.z, result['projects'])
