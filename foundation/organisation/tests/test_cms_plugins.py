import collections

from cms.test_utils.testcases import CMSTestCase

from ..models import Theme, Project, FeaturedProject
from ..cms_plugins import FeaturedProjectPlugin


class FeaturedProjectPluginTest(CMSTestCase):

    def setUp(self):  # flake8: noqa
        super(FeaturedProjectPluginTest, self).setUp()

        self.theme = Theme.objects.create(name='Secret Operations')
        self.project = Project.objects.create(name='Project X',
            description="I could tell you, but then I'd have to kill you.",
            theme=self.theme)
        self.featured = FeaturedProject.objects.create(project=self.project)

    def test_adds_project_to_context(self):
        plug = FeaturedProjectPlugin()
        result = plug.render({}, self.featured, 'foo')

        self.assertEqual(self.project, result['project'])
