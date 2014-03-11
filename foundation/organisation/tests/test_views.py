from django.core.urlresolvers import reverse
from django.utils.html import escape
from django.test.utils import override_settings
from django_webtest import WebTest

from ..models import (Board, Person, Project, Unit, Theme, WorkingGroup,
                      BoardMembership, UnitMembership)


@override_settings(ROOT_URLCONF='foundation.tests.urls')
class UnitListViewTest(WebTest):
    def setUp(self):  # flake8: noqa
        self.leonardo = Person.objects.create(
            name="Leonardo (Leo)",
            description='Turtle with a blue mask',
            email='leonardo@tmnt.org')
        self.raphael = Person.objects.create(
            name="Raphael (Raph)",
            description='Turtle with a red mask',
            email='raphael@tmnt.org',
            twitter='raph',
            url='http://tmnt.org/raphael')
        self.rocksteady = Person.objects.create(
            name="Rocksteady",
            description='Mutant rhinoceros',
            email='rocksteady@shreddercorp.org',
            twitter='rocksteady',
            url='http://beboprocksteady.com')
        self.april = Person.objects.create(
            name="April O'Neil",
            description='Computer Programmer',
            email='april@oneil.me',
            twitter='april',
            url='http://oneil.me')
        self.splinter = Person.objects.create(
            name="Splinter",
            description='Ninja rat',
            email='splinter@tmnt.org')

        self.turtles = Unit.objects.create(name="Turtles")
        self.footclan = Unit.objects.create(name="Foot Clan")
        self.masters = Unit.objects.create(name="Ninja Masters", order=1)

        self.turtle_leonardo = UnitMembership.objects.create(
            title='Leader',
            person=self.leonardo,
            unit=self.turtles)

        self.turtle_raphael = UnitMembership.objects.create(
            title='Bad boy',
            person=self.raphael,
            unit=self.turtles)

        self.evil_rocksteady = UnitMembership.objects.create(
            title='Comic relief',
            person=self.rocksteady,
            unit=self.footclan)

        self.master_splinter = UnitMembership.objects.create(
            title='Master',
            person=self.splinter,
            unit=self.masters)

    def test_units_in_response(self):
        response = self.app.get(reverse('units'))
        self.assertTrue(self.turtles.name in response)
        self.assertTrue(self.footclan.name in response)

    def test_unit_member_in_response(self):
        response = self.app.get(reverse('units'))
        self.assertTrue(self.leonardo.name in response)
        self.assertTrue(self.raphael.name in response)
        self.assertTrue(self.rocksteady.name in response)

    def test_non_unit_member_not_in_response(self):
        response = self.app.get(reverse('units'))
        self.assertTrue(self.april.name not in response)

    def test_unit_members_in_units(self):
        response = self.app.get(reverse('units'))
        footclan = response.body.find(self.footclan.name)
        turtles = response.body.find(self.turtles.name)

        # Units are ordered alphabetically
        self.assertTrue(footclan < turtles)
        leonardo = response.body.find(self.leonardo.name)
        raphael = response.body.find(self.raphael.name)
        rocksteady = response.body.find(self.rocksteady.name)
        self.assertTrue(footclan < rocksteady < turtles)
        self.assertTrue(turtles < leonardo < raphael)

    def test_description_in_response(self):
        response = self.app.get(reverse('units'))
        self.assertTrue(self.leonardo.description in response)
        self.assertTrue(self.raphael.description in response)
        self.assertTrue(self.rocksteady.description in response)
        self.assertTrue(self.april.description not in response)

    def test_email_in_response(self):
        response = self.app.get(reverse('units'))
        self.assertTrue(self.leonardo.email in response)
        self.assertTrue(self.raphael.email in response)
        self.assertTrue(self.rocksteady.email in response)
        self.assertTrue(self.april.email not in response)

    def test_twitter_in_response(self):
        response = self.app.get(reverse('units'))
        twitter_url = 'http://twitter.com/{handle}'
        twitter_raphael = twitter_url.format(handle=self.raphael.twitter)
        twitter_rocksteady = twitter_url.format(handle=self.rocksteady.twitter)
        twitter_april = twitter_url.format(handle=self.april.twitter)
        self.assertTrue(twitter_raphael in response)
        self.assertTrue(twitter_rocksteady in response)
        self.assertTrue(twitter_april not in response)

        # Raphael is the last turtle. We assume that the unit list will be
        # where the first occurance of the names come up (since main content
        # should come before sidebars).
        # Leonardo doesn't use Twitter so there shouldn't be a twitter url
        # between the last Leo's name and Raph's name
        leonardo = response.body.find(self.leonardo.name)
        raphael = response.body.find(self.raphael.name)
        twitter = response.body.find('http://twitter.com/', leonardo, raphael)
        self.assertTrue(twitter == -1)

    def test_url_in_response(self):
        response = self.app.get(reverse('units'))

        self.assertTrue(self.raphael.url in response)
        self.assertTrue(self.rocksteady.url in response)
        self.assertTrue(self.april.url not in response)

        # Raphael is the last turtle. We assume that the unit list will be
        # where the first occurance of the names come up (since main content
        # should come before sidebars).
        # Leonardo doesn't have a website so there shouldn't be a
        # 'Personal website' between the last Leo's name and Raph's name

        leonardo = response.body.find(self.leonardo.name)
        raphael = response.body.find(self.raphael.name)
        website = response.body.find('Personal website', leonardo, raphael)
        self.assertTrue(website == -1)

    def test_manual_order_of_units(self):
        response = self.app.get(reverse('units'))
        masters = response.body.find(self.masters.name)
        turtles = response.body.find(self.turtles.name)
        footclan = response.body.find(self.footclan.name)

        self.assertTrue(masters < footclan < turtles)


@override_settings(ROOT_URLCONF='foundation.tests.urls')
class BoardViewTest(WebTest):
    def setUp(self):  # flake8: noqa
        self.leonardo = Person.objects.create(
            name="Leonardo (Leo)",
            description='Turtle with a blue mask',
            email='leonardo@tmnt.org')
        self.april = Person.objects.create(
            name="April O'Neil",
            description='Computer Programmer',
            email='april@oneil.me',
            twitter='april',
            url='http://oneil.me')
        self.casey = Person.objects.create(
            name="Casey Jones",
            description='Hockey mask wearing vigilante',
            email='casey.jones@newyorkcricketclub.com',
            twitter='arnold')
        self.splinter = Person.objects.create(
            name="Splinter",
            description='Ninja rat',
            email='splinter@tmnt.org')

        self.board = Board.objects.create(
            name='Board of directors',
            slug='board',
            description='The board consists of a rat')
        self.council = Board.objects.create(
            name='Advisory Council',
            slug='advisory-board',
            description='Get a room you two!')

        self.rat_board = BoardMembership.objects.create(
            title='Director',
            person=self.splinter,
            board=self.board)

        self.april_council = BoardMembership.objects.create(
            title='Technical consultant',
            person=self.april,
            board=self.council)
        self.casey_council = BoardMembership.objects.create(
            title='Sport utilities consultant',
            person=self.casey,
            board=self.council)

    def test_board(self):
        response = self.app.get(reverse('board'))
        self.assertTrue(self.board.name in response.body)
        self.assertTrue(self.board.description in response.body)

        self.assertTrue(self.council.name not in response.body)

        self.assertTrue(self.splinter.name in response.body)
        self.assertTrue(self.rat_board.title in response.body)
        self.assertTrue(self.splinter.description in response.body)
        self.assertTrue(self.splinter.email not in response.body)

        self.assertTrue(self.casey.name not in response.body)
        self.assertTrue(self.april.name not in response.body)

    def test_advisory_council(self):
        response = self.app.get(reverse('advisory-board'))
        self.assertTrue(self.council.name in response.body)
        self.assertTrue(self.council.description in response.body)

        self.assertTrue(self.board.name not in response.body)

        # April's name must be escaped because of the single quote in O'Neil
        self.assertTrue(escape(self.april.name) in response.body)
        self.assertTrue(self.april_council.title in response.body)
        self.assertTrue(self.april.description in response.body)
        self.assertTrue(self.april.email not in response.body)
        self.assertTrue(self.april.twitter in response.body)
        self.assertTrue(self.april.url in response.body)

        self.assertTrue(self.casey.name in response.body)
        self.assertTrue(self.casey_council.title in response.body)
        self.assertTrue(self.casey.description in response.body)
        self.assertTrue(self.casey.email not in response.body)
        self.assertTrue(self.casey.twitter in response.body)

        self.assertTrue(self.splinter.name not in response.body)


@override_settings(ROOT_URLCONF='foundation.tests.urls')
class ProjectListViewTest(WebTest):
    def setUp(self):  # flake8: noqa
        self.market_garden = Project.objects.create(
            name='Market Garden',
            slug='market-garden',
            description='Just some guys in a glider')

        self.barbarossa = Project.objects.create(
            name='Barbarossa',
            slug='barbarossa',
            description='This could get cold quickly.')

    def test_projects_listed(self):
        response = self.app.get(reverse('projects'))

        self.assertIn(self.market_garden.name, response)
        self.assertIn(self.barbarossa.name, response)


@override_settings(ROOT_URLCONF='foundation.tests.urls')
class ProjectDetailViewTest(WebTest):
    def setUp(self):  # flake8: noqa
        self.market_garden = Project.objects.create(
            name='Market Garden',
            slug='market-garden',
            description='Just some guys in a glider')

        self.barbarossa = Project.objects.create(
            name='Barbarossa',
            slug='barbarossa',
            description='This could get cold quickly.')

    def test_project_detail(self):
        response = self.app.get(reverse('project',
                                        kwargs={'slug': 'market-garden'}))

        self.assertIn(self.market_garden.name, response)


@override_settings(ROOT_URLCONF='foundation.tests.urls')
class WorkingGroupListViewTest(WebTest):
    def setUp(self):  # flake8: noqa
        self.theme = Theme.objects.create(name='World Wide Web')

        self.csv = WorkingGroup.objects.create(
            name='CSV on the Web',
            slug='csv-on-the-web',
            description='Definition of a vocabulary for describing tables',
            url='http://www.w3.org/2013/csvw/',
            theme=self.theme,
            incubation=False
            )

        self.government = WorkingGroup.objects.create(
            name='Government Linked Data',
            slug='government-linked-data',
            description='Help governments around the world publish their data',
            url='http://www.w3.org/2011/gld/',
            theme=self.theme,
            incubation=True
            )

    def test_workinggroup_list(self):
        response = self.app.get(reverse('working-groups'))
        
        self.assertIn(self.csv.name, response)
        self.assertIn(self.csv.description, response)
        self.assertIn(self.csv.url, response)
        
        self.assertIn(self.government.name, response)
        self.assertIn(self.government.url, response)
        self.assertNotIn(self.government.description, response)
        
        # Active working groups should come before incubating groups
        csv = response.body.find(self.csv.name)
        government = response.body.find(self.government.name)
        self.assertTrue(csv < government)
