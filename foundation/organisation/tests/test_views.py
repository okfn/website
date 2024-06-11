from io import StringIO

from django.urls import reverse
from django_webtest import WebTest

from iso3166 import countries
import csv

from ..models import (
    Person,
    NetworkGroup,
    NetworkGroupMembership,
    NowDoing,
)


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
