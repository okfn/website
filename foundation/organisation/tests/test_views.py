from io import StringIO

from django.urls import reverse
from django.utils.html import escape
from django_webtest import WebTest
from unittest import skip

from iso3166 import countries
import csv

from ..models import (
    Board,
    Person,
    Unit,
    NetworkGroup,
    NetworkGroupMembership,
    BoardMembership,
    UnitMembership,
    NowDoing,
)


class UnitListViewTest(WebTest):
    def setUp(self):
        self.donatello = Person.objects.create(
            name="Donatello (Donnie)",
            description="Turtle with a purple mask",
            email="donatello@tmnt.org",
        )
        self.leonardo = Person.objects.create(
            name="Leonardo (Leo)",
            description="Turtle with a blue mask",
            email="leonardo@tmnt.org",
        )
        self.raphael = Person.objects.create(
            name="Raphael (Raph)",
            description="Turtle with a red mask",
            email="raphael@tmnt.org",
            twitter="raph",
            url="http://tmnt.org/raphael",
        )
        self.rocksteady = Person.objects.create(
            name="Rocksteady",
            description="Mutant rhinoceros",
            email="rocksteady@shreddercorp.org",
            twitter="rocksteady",
            url="http://beboprocksteady.com",
        )
        self.april = Person.objects.create(
            name="April O'Neil",
            description="Computer Programmer",
            email="april@oneil.me",
            twitter="april",
            url="http://oneil.me",
        )
        self.splinter = Person.objects.create(
            name="Splinter", description="Ninja rat", email="splinter@tmnt.org"
        )

        self.turtles = Unit.objects.create(name="Turtles")
        self.footclan = Unit.objects.create(name="Foot Clan")
        self.masters = Unit.objects.create(name="Ninja Masters", order=1)

        self.turtle_donatello = UnitMembership.objects.create(
            title="Hacker", person=self.donatello, unit=self.turtles
        )

        self.turtle_leonardo = UnitMembership.objects.create(
            title="Leader", person=self.leonardo, unit=self.turtles, order=1
        )

        self.turtle_raphael = UnitMembership.objects.create(
            title="Bad boy", person=self.raphael, unit=self.turtles
        )

        self.evil_rocksteady = UnitMembership.objects.create(
            title="Comic relief", person=self.rocksteady, unit=self.footclan
        )

        self.master_splinter = UnitMembership.objects.create(
            title="Master", person=self.splinter, unit=self.masters
        )

    def test_units_in_response(self):
        response = self.app.get(reverse("units"))
        self.assertTrue(self.turtles.name in response)
        self.assertTrue(self.footclan.name in response)

    def test_unit_member_in_response(self):
        response = self.app.get(reverse("units"))
        self.assertTrue(self.leonardo.name in response)
        self.assertTrue(self.raphael.name in response)
        self.assertTrue(self.rocksteady.name in response)

    def test_non_unit_member_not_in_response(self):
        response = self.app.get(reverse("units"))
        self.assertTrue(self.april.name not in response)

    def test_unit_members_in_units(self):
        response = self.app.get(reverse("units"))

        # Units are ordered alphabetically
        footclan = response.text.find(self.footclan.name)
        turtles = response.text.find(self.turtles.name)
        self.assertTrue(footclan < turtles)

        # Unit members are ordered alphabetically
        # unless order is overwritten
        donatello = response.text.find(self.donatello.name)
        leonardo = response.text.find(self.leonardo.name)
        raphael = response.text.find(self.raphael.name)
        rocksteady = response.text.find(self.rocksteady.name)
        self.assertTrue(footclan < rocksteady < turtles)
        self.assertTrue(turtles < leonardo < donatello < raphael)

    def test_description_in_response(self):
        response = self.app.get(reverse("units"))
        self.assertTrue(self.leonardo.description in response)
        self.assertTrue(self.raphael.description in response)
        self.assertTrue(self.rocksteady.description in response)
        self.assertTrue(self.april.description not in response)

    def test_email_in_response(self):
        response = self.app.get(reverse("units"))
        self.assertTrue(self.leonardo.email in response)
        self.assertTrue(self.raphael.email in response)
        self.assertTrue(self.rocksteady.email in response)
        self.assertTrue(self.april.email not in response)

    def test_twitter_in_response(self):
        response = self.app.get(reverse("units"))
        twitter_url = "https://twitter.com/{handle}"
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
        leonardo = response.text.find(self.leonardo.name)
        raphael = response.text.find(self.raphael.name)
        twitter = response.text.find("https://twitter.com/", leonardo, raphael)
        self.assertTrue(twitter == -1)

    @skip("Broken after the 2019 update")
    def test_url_in_response(self):
        response = self.app.get(reverse("units"))

        self.assertTrue(self.raphael.url in response)
        self.assertTrue(self.rocksteady.url in response)
        self.assertTrue(self.april.url not in response)

        # Raphael is the last turtle. We assume that the unit list will be
        # where the first occurance of the names come up (since main content
        # should come before sidebars).
        # Leonardo doesn't have a website so there shouldn't be a
        # 'Personal website' between the last Leo's name and Raph's name

        leonardo = response.text.find(self.leonardo.name)
        raphael = response.text.find(self.raphael.name)
        website = response.text.find("Personal website", leonardo, raphael)
        self.assertTrue(website == -1)

    def test_manual_order_of_units(self):
        response = self.app.get(reverse("units"))
        masters = response.text.find(self.masters.name)
        turtles = response.text.find(self.turtles.name)
        footclan = response.text.find(self.footclan.name)

        self.assertTrue(masters < footclan < turtles)


class BoardViewTest(WebTest):
    def setUp(self):
        self.leonardo = Person.objects.create(
            name="Leonardo (Leo)",
            description="Turtle with a blue mask",
            email="leonardo@tmnt.org",
        )
        self.april = Person.objects.create(
            name="April O'Neil",
            description="Computer Programmer",
            email="april@oneil.me",
            twitter="april",
            url="http://oneil.me",
        )
        self.casey = Person.objects.create(
            name="Casey Jones",
            description="Hockey mask wearing vigilante",
            email="casey.jones@newyorkcricketclub.com",
            twitter="arnold",
        )
        self.splinter = Person.objects.create(
            name="Splinter", description="Ninja rat", email="splinter@tmnt.org"
        )

        self.board = Board.objects.create(
            name="Board of directors",
            slug="board",
            description="The board consists of a rat",
        )
        self.council = Board.objects.create(
            name="Advisory Council",
            slug="advisory-board",
            description="Get a room you two!",
        )

        self.rat_board = BoardMembership.objects.create(
            title="Director", person=self.splinter, board=self.board
        )

        self.april_council = BoardMembership.objects.create(
            title="Technical consultant", person=self.april, board=self.council, order=2
        )
        self.casey_council = BoardMembership.objects.create(
            title="Sport utilities consultant",
            person=self.casey,
            board=self.council,
            order=1,
        )
        self.leonardo_council = BoardMembership.objects.create(
            title="Medical consultant",
            person=self.leonardo,
            board=self.council,
            order=3,
        )

    @skip("Broken after the 2019 update")
    def test_board(self):
        response = self.app.get(reverse("board"))
        self.assertTrue(self.board.name in response.text)
        self.assertTrue(self.board.description in response.text)

        self.assertTrue(self.council.name not in response.text)

        self.assertTrue(self.splinter.name in response.text)
        self.assertTrue(self.rat_board.title in response.text)
        self.assertTrue(self.splinter.description in response.text)
        self.assertTrue(self.splinter.email not in response.text)

        self.assertTrue(self.casey.name not in response.text)
        self.assertTrue(self.april.name not in response.text)

    @skip("Broken after the 2019 update")
    def test_advisory_council(self):
        response = self.app.get(reverse("advisory-board"))
        self.assertTrue(self.council.name in response.text)
        self.assertTrue(self.council.description in response.text)

        self.assertTrue(self.board.name not in response.text)

        # April's name must be escaped because of the single quote in O'Neil
        self.assertTrue(escape(self.april.name) in response.text)
        self.assertTrue(self.april_council.title in response.text)
        self.assertTrue(self.april.description in response.text)
        self.assertTrue(self.april.email not in response.text)
        self.assertTrue(self.april.twitter in response.text)
        self.assertTrue(self.april.url in response.text)

        self.assertTrue(self.casey.name in response.text)
        self.assertTrue(self.casey_council.title in response.text)
        self.assertTrue(self.casey.description in response.text)
        self.assertTrue(self.casey.email not in response.text)
        self.assertTrue(self.casey.twitter in response.text)

        self.assertTrue(self.splinter.name not in response.text)

    def test_manual_order_of_units(self):
        response = self.app.get(reverse("advisory-board"))
        april = response.text.find(escape(self.april.name))
        leonardo = response.text.find(self.leonardo.name)
        casey = response.text.find(self.casey.name)
        self.assertTrue(leonardo < april < casey)


class NetworkGroupDetailViewTest(WebTest):
    def setUp(self):
        self.otto = Person.objects.create(
            name="Otto von Bismarck",
            description="The oldest member and Duke of Lauenburg",
            email="bismarck@bismarck.org",
            twitter="busymark",
            url="http://betterthanwinston.de",
        )

        self.winston = Person.objects.create(
            name="Sir Winston Churchill",
            description="Grandson of the 7th Duke of Marlborough",
            email="winston@okfn.org",
            twitter="ftw_stn",
            url="http://forthewinston.org",
        )

        self.elizabeth = Person.objects.create(
            name="Elizabeth Angela Marguerite Bowes-Lyon",
            description="I am no duke, I am the queen",
            email="queen@monarch.me",
            twitter="thequeen",
            url="http://monarch.me/",
        )

        self.britain = NetworkGroup.objects.create(
            name="Open Knowledge Foundation Britain",
            group_type=0,  # local group
            description="Bisquits, tea, and open data",
            country="GB",
            mailinglist_url="http://lists.okfn.org/okfn-britain",
            homepage_url="http://gb.okfn.org/",
            twitter="OKFNgb",
        )

        self.buckingham = NetworkGroup.objects.create(
            name="Open Knowledge Buckingham",
            group_type=0,  # local group
            description="We run the Open Palace project",
            country="GB",
            region="Buckingham",
            homepage_url="http://queen.okfn.org/",
            twitter="buckingham",
            facebook_url="http://facebook.com/queenthepersonnottheband",
        )

        self.germany = NetworkGroup.objects.create(
            name="Open Knowledge Foundation Germany",
            group_type=1,  # chapter
            description="Haben Sie ein Kugelschreiber bitte?",
            country="DE",
            mailinglist_url="http://lists.okfn.org/okfn-de",
            homepage_url="http://de.okfn.org/",
            twitter="OKFNde",
        )

        self.otto_germany = NetworkGroupMembership.objects.create(
            networkgroup=self.germany, person=self.otto, title="First chancellor"
        )

        self.winston_britain = NetworkGroupMembership.objects.create(
            networkgroup=self.britain,
            person=self.winston,
            title="Prime minister with intervals",
        )

        self.elizabeth_britain = NetworkGroupMembership.objects.create(
            networkgroup=self.buckingham, person=self.elizabeth, title="Regent maker"
        )

    def test_country_group(self):
        response = self.app.get(
            reverse("network-country", kwargs={"country": self.britain.country_slug})
        )

        self.assertIn(self.britain.name, response.text)
        # TODO test skipped until we define if "britain" must be
        # included here
        # self.assertIn(self.britain.get_group_type_display().lower(),
        #               response.text.lower())
        # self.assertIn(self.britain.description, response.text)
        # self.assertIn(self.britain.get_country_display(), response.text)
        # self.assertIn(self.britain.homepage_url, response.text)
        # self.assertIn(self.britain.mailinglist_url, response.text)
        # self.assertIn(self.britain.twitter, response.text)

        self.assertNotIn(
            self.germany.get_group_type_display().lower(), response.text.lower()
        )

        self.assertIn(self.winston.name, response.text)
        self.assertIn(self.winston_britain.title, response.text)
        self.assertIn(self.elizabeth.name, response.text)
        self.assertIn(self.elizabeth_britain.title, response.text)
        self.assertNotIn(self.otto.name, response.text)

        # TODO test skipped until we define if "buckingham" must be
        # included here
        # self.assertIn(self.buckingham.name, response.text)
        # self.assertNotIn(self.buckingham.description, response.text)
        self.assertNotIn(self.germany.name, response.text)

    def test_regional_group(self):
        response = self.app.get(
            reverse(
                "network-region",
                kwargs={
                    "country": self.buckingham.country_slug,
                    "region": self.buckingham.region_slug,
                },
            )
        )

        self.assertIn(self.buckingham.name, response.text)

        # TODO test skipped until we define if "buckingham" must be
        # included here
        # self.assertIn(self.buckingham.description, response.text)
        # self.assertIn(self.buckingham.get_country_display(), response.text)
        # self.assertIn(self.buckingham.region, response.text)
        # self.assertIn(self.buckingham.homepage_url, response.text)
        # self.assertIn(self.buckingham.twitter, response.text)
        # self.assertIn(self.buckingham.facebook_url, response.text)
        # self.assertIn(
        #     reverse(
        #         'network-country',
        #         kwargs={'country': self.buckingham.country_slug}
        #     ),
        #     response.text
        # )
        self.assertNotIn(self.britain.homepage_url, response.text)
        self.assertNotIn(self.britain.mailinglist_url, response.text)
        self.assertNotIn(self.britain.twitter, response.text)

        self.assertIn(self.elizabeth.name, response.text)
        self.assertIn(self.elizabeth_britain.title, response.text)
        self.assertNotIn(self.winston.name, response.text)
        self.assertNotIn(self.otto.name, response.text)

        self.assertNotIn(self.britain.description, response.text)
        self.assertNotIn(self.germany.name, response.text)

    def test_csv_output(self):
        response = self.app.get(reverse("networkgroups-csv"))
        reader = csv.reader(StringIO(response.text))

        header_row = next(reader)

        # Headers need to be on a specific form
        headers = [
            "ISO3",
            "Country",
            "Map location",
            "Local Groups status",
            "Community Leaders",
            "Website",
            "Mailing List",
            "Twitter handle",
            "Facebook page",
        ]

        self.assertEqual(header_row, headers)

        germany = next(reader)
        germany_data = [
            countries.get(self.germany.country.code).alpha3,
            self.germany.get_country_display(),
            "",
            self.germany.get_group_type_display(),
            ", ".join([m.name for m in self.germany.members.all()]),
            self.germany.homepage_url,
            self.germany.mailinglist_url,
            self.germany.twitter,
            "",
        ]
        self.assertEqual(germany, germany_data)

        britain = next(reader)
        britain_data = [
            countries.get(self.britain.country.code).alpha3,
            self.britain.get_country_display(),
            "",
            self.britain.get_group_type_display(),
            ", ".join([m.name for m in self.britain.members.all()]),
            self.britain.homepage_url,
            self.britain.mailinglist_url,
            self.britain.twitter,
            "",
        ]
        self.assertEqual(britain, britain_data)

        buckingham = next(reader)
        buckingham_data = [
            countries.get(self.buckingham.country.code).alpha3,
            self.buckingham.get_country_display(),
            "{region}, {country}".format(
                region=self.buckingham.region,
                country=self.buckingham.get_country_display(),
            ),
            self.buckingham.get_group_type_display(),
            ", ".join([m.name for m in self.buckingham.members.all()]),
            self.buckingham.homepage_url,
            self.buckingham.mailinglist_url,
            self.buckingham.twitter,
            self.buckingham.facebook_url,
        ]
        self.assertEqual(buckingham, buckingham_data)

    def test_NowDoing_icon_name_works(self, *args):  # noqa
        donatello = Person.objects.create(
            name="Donatello (Donnie)",
            username_on_slack="donnie",
            description="Turtle with a purple mask",
            email="donatello@tmnt.org",
        )
        donatello.save()

        watching = NowDoing.objects.create(
            person=donatello, doing_type="watching", text="a movie"
        )
        watching.save()

        location = NowDoing.objects.create(
            person=donatello, doing_type="location", text="Berlin"
        )
        watching.save()

        self.assertEqual(watching.icon_name, "playing")
        self.assertEqual(location.icon_name, "location")

    def test_NowDoing_display_name(self, *args):  # noqa
        donatello = Person.objects.create(
            name="Donatello (Donnie)",
            username_on_slack="donnie",
            description="Turtle with a purple mask",
            email="donatello@tmnt.org",
        )
        donatello.save()

        watching = NowDoing.objects.create(
            person=donatello, doing_type="watching", text="a movie"
        )
        watching.save()

        listening = NowDoing.objects.create(
            person=donatello, doing_type="listening", text="The beatles"
        )
        watching.save()

        self.assertEqual(listening.display_name, "Listening to")
        self.assertEqual(watching.display_name, "Watching")
