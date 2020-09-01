from cms.test_utils.testcases import CMSTestCase
from cms.models.pluginmodel import CMSPlugin

from ..models import (Project, ProjectType, Theme, NetworkGroup,
                      NetworkGroupList)
from ..models import FeaturedProject, ProjectList, SignupForm
from ..cms_plugins import (FeaturedProjectPlugin, ProjectListPlugin,
                           ThemesPlugin, NetworkGroupFlagsPlugin,
                           SignupFormPlugin)


class FeaturedProjectPluginTest(CMSTestCase):

    def setUp(self):
        super().setUp()

        self.project = Project.objects.create(
            name='Project X',
            description="I could tell you, but then I'd have to kill you."
        )
        self.featured = FeaturedProject.objects.create(project=self.project)

    def test_adds_project_to_context(self):
        plug = FeaturedProjectPlugin()
        result = plug.render({}, self.featured, 'foo')

        self.assertEqual(self.project, result['project'])


class ProjectListPluginTest(CMSTestCase):

    def setUp(self):
        super().setUp()

        self.cheese = Theme.objects.create(name='Cheese')
        self.programming = ProjectType.objects.create(name='Programming')

        self.x = Project.objects.create(
            name='Project X',
            slug='project-x',
            description="I could tell you, but then I'd have to kill you."
        )
        self.y = Project.objects.create(
            name='Project Y',
            slug='project-y',
            description="Why, why, why?"
        )
        self.z = Project.objects.create(
            name='Project Z',
            slug='project-z',
            description="I do believe it. I do believe it's true."
        )

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


class ThemePluginTest(CMSTestCase):

    def setUp(self):
        super().setUp()

        self.hats = Theme.objects.create(
            name='Hats',
            slug='hats',
            blurb='People must wear hats to the party',
            description='Any hat goes but Red Hat or Fedora get extra points')

        self.orange = Theme.objects.create(
            name='Orange clothes',
            slug='orange-clothes',
            blurb='People must wear orange clothes to the party',
            description='Come dressed as an orange for extra points')

        self.instance = CMSPlugin()

    def test_theme_plugin(self):
        plug = ThemesPlugin()
        result = plug.render({}, self.instance, 'foo')

        self.assertIn(self.hats, result['object_list'])
        self.assertIn(self.orange, result['object_list'])


class NetworkGroupPluginTest(CMSTestCase):

    def setUp(self):
        super().setUp()

        self.britain = NetworkGroup.objects.create(
            name='Open Knowledge Foundation Britain',
            group_type=0,  # local group
            description='Bisquits, tea, and open data',
            country='GB',
            mailinglist_url='http://lists.okfn.org/okfn-britain',
            homepage_url='http://gb.okfn.org/',
            twitter='OKFNgb'
        )

        self.buckingham = NetworkGroup.objects.create(
            name='Open Knowledge Buckingham',
            group_type=0,  # local group
            description='We run the Open Palace project',
            country='GB',
            region='Buckingham',
            homepage_url='http://queen.okfn.org/',
            twitter='buckingham',
            facebook_url='http://facebook.com/queenthepersonnottheband',
        )

        self.germany = NetworkGroup.objects.create(
            name='Open Knowledge Foundation Germany',
            group_type=1,  # chapter
            description='Haben Sie ein Kugelschreiber bitte?',
            country='DE',
            mailinglist_url='http://lists.okfn.org/okfn-de',
            homepage_url='http://de.okfn.org/',
            twitter='OKFNde'
        )

        self.switzerland = NetworkGroup.objects.create(
            name='Open Knowledge Foundation Switzerland',
            group_type=1,  # chapter
            description='Switzerland loves open data',
            country='CH',
            mailinglist_url='http://lists.okfn.org/okfn-ch',
            homepage_url='http://opendata.ch',
        )

        self.localgroups = NetworkGroupList(group_type=0)
        self.chapters = NetworkGroupList(group_type=1)

    def test_localgroups_plugin(self):
        plug = NetworkGroupFlagsPlugin()
        result = plug.render({}, self.localgroups, 'foo')

        self.assertSequenceEqual(sorted(result['countries'],
                                        key=lambda group: group.name),
                                 result['countries'])
        self.assertIn(self.britain, result['countries'])
        self.assertNotIn(self.germany, result['countries'])
        self.assertNotIn(self.buckingham, result['countries'])

    def test_chapters_plugin(self):
        plug = NetworkGroupFlagsPlugin()
        result = plug.render({}, self.chapters, 'foo')

        self.assertSequenceEqual(sorted(result['countries'],
                                        key=lambda chapter: chapter.name),
                                 result['countries'])
        self.assertNotIn(self.britain, result['countries'])
        self.assertIn(self.germany, result['countries'])
        self.assertNotIn(self.buckingham, result['countries'])


class SignupFormPluginTest(CMSTestCase):

    def setUp(self):
        super().setUp()

        self.loveme = SignupForm.objects.create(
            title='Love me',
            description='Tell me, do.')

    def test_title_description_added_to_signupform_plugin(self):
        plug = SignupFormPlugin()
        result = plug.render({}, self.loveme, 'foo')

        self.assertEqual('Love me', result['title'])
        self.assertEqual('Tell me, do.', result['description'])
