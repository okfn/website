from django.core.urlresolvers import reverse
from django.utils.html import escape
from django.test.utils import override_settings
from django_webtest import WebTest

from geoposition import Geoposition
from iso3166 import countries
from StringIO import StringIO
import unicodecsv

from ..models import (Board, Person, Project, Unit, Theme, WorkingGroup,
                      NetworkGroup, NetworkGroupMembership,
                      BoardMembership, UnitMembership)


@override_settings(ROOT_URLCONF='foundation.tests.urls')
class UnitListViewTest(WebTest):
    def setUp(self):  # flake8: noqa
        self.donatello = Person.objects.create(
            name="Donatello (Donnie)",
            description='Turtle with a purple mask',
            email='donatello@tmnt.org')
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

        self.turtle_donatello = UnitMembership.objects.create(
            title='Hacker',
            person=self.donatello,
            unit=self.turtles)

        self.turtle_leonardo = UnitMembership.objects.create(
            title='Leader',
            person=self.leonardo,
            unit=self.turtles,
            order=1)

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

        # Units are ordered alphabetically
        footclan = response.body.find(self.footclan.name)
        turtles = response.body.find(self.turtles.name)
        self.assertTrue(footclan < turtles)

        # Unit members are ordered alphabetically
        # unless order is overwritten
        donatello = response.body.find(self.donatello.name)
        leonardo = response.body.find(self.leonardo.name)
        raphael = response.body.find(self.raphael.name)
        rocksteady = response.body.find(self.rocksteady.name)
        self.assertTrue(footclan < rocksteady < turtles)
        self.assertTrue(turtles < leonardo < donatello < raphael)

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
class ThemeDetailViewTest(WebTest):
    def setUp(self):  # flake8: noqa
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

        self.kernel = WorkingGroup.objects.create(
            name='Kernel people',
            slug='kernel-people',
            description='Linus disciples',
            homepage_url='http://kernel.org')
        self.kernel.themes.add(self.hats)

        self.i18n = WorkingGroup.objects.create(
            name='Internationalisation',
            slug='i18n',
            description='I prefer my own language thank you',
            homepage_url='https://fedoraproject.org/wiki/I18N',
            incubation=True)
        self.i18n.themes.add(self.hats)

        self.beefy = Project.objects.create(
            name='Beefy Miracle',
            slug='beefy-miracle',
            teaser='Does the number 17 mean anything to you?',
            description='Mmmmm... edible projects',
            homepage_url='https://fedoraproject.org/wiki/Beefy_Miracle')

        self.beefy.themes.add(self.hats)

    def test_theme_page(self):
        response = self.app.get(
            reverse('theme', kwargs={'slug': self.hats.slug}))

        self.assertIn(self.hats.name, response)
        self.assertIn(self.hats.blurb, response)
        self.assertIn(self.hats.description, response)

        self.assertIn(self.kernel.name, response)
        self.assertIn(self.kernel.description, response)
        self.assertIn(self.kernel.homepage_url, response)
        # Incubating groups should also show up
        self.assertIn(self.i18n.name, response)

        self.assertIn(self.beefy.name, response)
        self.assertIn(self.beefy.teaser, response)
        self.assertIn(self.beefy.get_absolute_url(), response)
        self.assertNotIn(self.beefy.description, response)

        self.assertIn(self.orange.name, response)
        self.assertIn(self.orange.get_absolute_url(), response)
        self.assertNotIn(self.orange.description, response)


@override_settings(ROOT_URLCONF='foundation.tests.urls')
class WorkingGroupListViewTest(WebTest):
    def setUp(self):  # flake8: noqa
        self.theme = Theme.objects.create(
            name='World Wide Web',
            slug='world-wide-web',
            blurb='That thing in the browser',
            description='This what people incorrectly call "The Internet"')

        self.csv = WorkingGroup.objects.create(
            name='CSV on the Web',
            slug='csv-on-the-web',
            description='Definition of a vocabulary for describing tables',
            homepage_url='http://www.w3.org/2013/csvw/',
            incubation=False)
        self.csv.themes.add(self.theme)

        self.government = WorkingGroup.objects.create(
            name='Government Linked Data',
            slug='government-linked-data',
            description='Help governments around the world publish their data',
            homepage_url='http://www.w3.org/2011/gld/',
            incubation=True)
        self.government.themes.add(self.theme)

    def test_workinggroup_list(self):
        response = self.app.get(reverse('working-groups'))

        self.assertIn(self.csv.name, response)
        self.assertIn(self.csv.description, response)
        self.assertIn(self.csv.homepage_url, response)

        self.assertIn(self.government.name, response)
        self.assertIn(self.government.homepage_url, response)
        self.assertNotIn(self.government.description, response)

        # Active working groups should come before incubating groups
        csv = response.body.find(self.csv.name)
        government = response.body.find(self.government.name)
        self.assertTrue(csv < government)

@override_settings(ROOT_URLCONF='foundation.tests.urls')
class NetworkGroupDetailViewTest(WebTest):
    def setUp(self):  # flake8: noqa

        self.government = WorkingGroup.objects.create(
            name='Open Government',
            slug='open-government',
            description='We work toward open governments around the world',
            homepage_url='http://opengov.org',
            incubation=False
            )

        self.lobbying = WorkingGroup.objects.create(
            name='Lobbying Transparency',
            slug='lobbying-transparency',
            description='We want hotel lobbies made out of glass',
            homepage_url='http://transparent.lobby.org',
            incubation=False
            )

        self.otto = Person.objects.create(
            name='Otto von Bismarck',
            description='The oldest member and Duke of Lauenburg',
            email='bismarck@bismarck.org',
            twitter='busymark',
            url='http://betterthanwinston.de'
            )

        self.winston = Person.objects.create(
            name='Sir Winston Churchill',
            description='Grandson of the 7th Duke of Marlborough',
            email='winston@okfn.org',
            twitter='ftw_stn',
            url='http://forthewinston.org'
            )

        self.elizabeth = Person.objects.create(
            name='Elizabeth Angela Marguerite Bowes-Lyon',
            description='I am no duke, I am the queen',
            email='queen@monarch.me',
            twitter='thequeen',
            url='http://monarch.me/'
            )

        self.britain = NetworkGroup.objects.create(
            name='Open Knowledge Foundation Britain',
            group_type=0, # local group
            description='Bisquits, tea, and open data',
            country='GB',
            mailinglist_url='http://lists.okfn.org/okfn-britain',
            homepage_url='http://gb.okfn.org/',
            wiki_url='http://wiki.okfn.org/GodSaveTheQueen',
            twitter='OKFNgb'
            )

        self.buckingham = NetworkGroup.objects.create(
            name='Open Knowledge Buckingham',
            group_type=0, # local group
            description='We run the Open Palace project',
            country='GB',
            region=u'Buckingham',
            position=Geoposition(51.501364, -0.141890),
            homepage_url='http://queen.okfn.org/',
            twitter='buckingham',
            facebook_url='http://facebook.com/queenthepersonnottheband',
            youtube_url='https://www.youtube.com/user/Queenovision',
            gplus_url='https://plus.google.com/+Intel',
            )


        self.germany = NetworkGroup.objects.create(
            name='Open Knowledge Foundation Germany',
            group_type=1, # chapter
            description='Haben Sie ein Kugelschreiber bitte?',
            country='DE',
            mailinglist_url='http://lists.okfn.org/okfn-de',
            homepage_url='http://de.okfn.org/',
            twitter='OKFNde'
            )

        self.otto_germany = NetworkGroupMembership.objects.create(
            networkgroup=self.germany,
            person=self.otto,
            title='First chancellor'
            )

        self.winston_britain = NetworkGroupMembership.objects.create(
            networkgroup=self.britain,
            person=self.winston,
            title='Prime minister with intervals'
            )

        self.elizabeth_britain = NetworkGroupMembership.objects.create(
            networkgroup=self.buckingham,
            person=self.elizabeth,
            title='Regent maker'
            )

        self.britain.working_groups.add(self.government)
        self.buckingham.working_groups.add(self.lobbying)
        self.germany.working_groups.add(self.government)
        self.germany.working_groups.add(self.lobbying)

    def test_country_group(self):
        response = self.app.get(
            reverse('network-country',
                    kwargs={'country': self.britain.country_slug}))

        self.assertIn(self.britain.name, response.body)

        self.assertIn(self.britain.get_group_type_display().lower(),
                      response.body.lower())
        self.assertNotIn(self.germany.get_group_type_display().lower(),
                         response.body.lower())

        self.assertIn(self.britain.description, response.body)
        self.assertIn(self.britain.get_country_display(), response.body)
        self.assertIn(self.britain.homepage_url, response.body)
        self.assertIn(self.britain.mailinglist_url, response.body)
        self.assertIn(self.britain.twitter, response.body)

        self.assertIn(self.winston.name, response.body)
        self.assertIn(self.winston_britain.title, response.body)
        self.assertIn(self.elizabeth.name, response.body)
        self.assertIn(self.elizabeth_britain.title, response.body)
        self.assertNotIn(self.otto.name, response.body)

        self.assertIn(self.buckingham.name, response.body)
        self.assertNotIn(self.buckingham.description, response.body)
        self.assertNotIn(self.germany.name, response.body)

    def test_regional_group(self):
        response = self.app.get(
            reverse('network-region',
                    kwargs={'country': self.buckingham.country_slug,
                            'region': self.buckingham.region_slug}))

        self.assertIn(self.buckingham.name, response.body)

        self.assertIn(self.buckingham.description, response.body)

        self.assertIn(self.buckingham.get_country_display(), response.body)
        self.assertIn(self.buckingham.region, response.body)

        self.assertIn(self.buckingham.homepage_url, response.body)
        self.assertNotIn(self.britain.homepage_url, response.body)
        self.assertNotIn(self.britain.wiki_url, response.body)
        self.assertNotIn(self.britain.mailinglist_url, response.body)
        self.assertIn(self.buckingham.twitter, response.body)
        self.assertNotIn(self.britain.twitter, response.body)
        self.assertIn(self.buckingham.facebook_url, response.body)
        self.assertIn(self.buckingham.youtube_url, response.body)
        self.assertIn(self.buckingham.gplus_url, response.body)

        self.assertIn(self.elizabeth.name, response.body)
        self.assertIn(self.elizabeth_britain.title, response.body)
        self.assertNotIn(self.winston.name, response.body)
        self.assertNotIn(self.otto.name, response.body)

        self.assertIn(reverse('network-country',
                              kwargs={'country':self.buckingham.country_slug}),
                      response.body)
        self.assertNotIn(self.britain.description, response.body)
        self.assertNotIn(self.germany.name, response.body)


    def test_workinggroups_in_networks(self):

        britain = self.app.get(
            reverse('network-country',
                    kwargs={'country': self.britain.country_slug}))

        # Britain is a single working group country and should not show
        # regional group working groups
        self.assertIn(self.government.name, britain.body)
        self.assertNotIn(self.lobbying.name, britain.body)

        buckingham = self.app.get(
            reverse('network-region',
                    kwargs={'country': self.buckingham.country_slug,
                            'region': self.buckingham.region_slug}))

        # Regional groups should not inherit working groups of country group
        self.assertIn(self.lobbying.name, buckingham.body)
        self.assertNotIn(self.government.name, buckingham.body)

        germany = self.app.get(
            reverse('network-country',
                    kwargs={'country': self.germany.country_slug}))

        # Germany has many groups and they should all be shown
        self.assertIn(self.government.name, germany.body)
        self.assertIn(self.lobbying.name, germany.body)

    def test_csv_output(self):
        response = self.app.get(reverse('networkgroups-csv'))
        csv = unicodecsv.reader(StringIO(response.body))

        header_row = csv.next()

        # Headers need to be on a specific form
        headers = ['ISO3', 'Country', 'Geo coordinates', 'Map location',
                   'Local Groups status', 'Community Leaders', 'Website',
                   'Wiki page', 'Mailing List', 'Twitter handle',
                   'Youtube channel', 'Facebook page', 'Google+ page']
        for group in WorkingGroup.objects.all():
            headers.append('Topic: {0}'.format(group.name))

        self.assertEqual(header_row, headers)

        germany = csv.next()
        germany_data = [countries.get(self.germany.country.code).alpha3,
                        self.germany.get_country_display(),
                        '', '', self.germany.get_group_type_display(),
                        ', '.join([m.name for m in self.germany.members.all()]),
                        self.germany.homepage_url,
                        self.germany.wiki_url,
                        self.germany.mailinglist_url,
                        self.germany.twitter, '', '',
                        self.germany.gplus_url, 'Y', 'Y']

        self.assertEqual(germany, germany_data)

        britain = csv.next()
        britain_data = [countries.get(self.britain.country.code).alpha3,
                        self.britain.get_country_display(),
                        '', '', self.britain.get_group_type_display(),
                        ', '.join([m.name for m in self.britain.members.all()]),
                        self.britain.homepage_url,
                        self.britain.wiki_url,
                        self.britain.mailinglist_url,
                        self.britain.twitter, '', '',
                        self.britain.gplus_url, '', 'Y']
        #import pdb; pdb.set_trace()
        self.assertEqual(britain, britain_data)

        buckingham = csv.next()
        buckingham_data = [
            countries.get(self.buckingham.country.code).alpha3,
            self.buckingham.get_country_display(),
            '{lat},{lon}'.format(
                lat=self.buckingham.position.latitude,
                lon=self.buckingham.position.longitude
                ),
            '{region}, {country}'.format(
                region=self.buckingham.region,
                country=self.buckingham.get_country_display()
                ),
            self.buckingham.get_group_type_display(),
            ', '.join([m.name for m in self.buckingham.members.all()]),
            self.buckingham.homepage_url,
            self.buckingham.mailinglist_url,
            self.buckingham.twitter,
            self.buckingham.youtube_url,
            self.buckingham.facebook_url, 'Y', '' '']
