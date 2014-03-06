import collections

from cms.test_utils.testcases import CMSTestCase

from ..models import Project, FeaturedProject
from ..cms_plugins import FeaturedProjectPlugin


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
