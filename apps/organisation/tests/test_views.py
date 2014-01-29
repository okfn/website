from django.core.urlresolvers import reverse
from django.test.utils import override_settings
from django_webtest import WebTest

from apps.organisation.models import Person, Unit, UnitMembership

@override_settings(ROOT_URLCONF='foundation.tests.urls')
class UnitListViewTest(WebTest):
    def setUp(self):
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

        self.turtles = Unit.objects.create(name="Turtles")
        self.footclan = Unit.objects.create(name="Foot Clan")

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

    def testUnitsInResponse(self):
        response = self.app.get(reverse('units-list'))
        self.assertTrue(self.turtles.name in response)
        self.assertTrue(self.footclan.name in response)

    def testUnitMemberInResponse(self):
        response = self.app.get(reverse('units-list'))
        self.assertTrue(self.leonardo.name in response)
        self.assertTrue(self.raphael.name in response)
        self.assertTrue(self.rocksteady.name in response)

    def testNonUnitMemberNotInResponse(self):
        response = self.app.get(reverse('units-list'))
        self.assertTrue(self.april.name not in response)

    def testUnitMembersInUnits(self):
        response = self.app.get(reverse('units-list'))
        footclan = response.body.find(self.footclan.name)
        turtles = response.body.find(self.turtles.name)

        # Units are ordered alphabetically
        self.assertTrue(footclan < turtles)
        leonardo = response.body.find(self.leonardo.name)
        raphael = response.body.find(self.raphael.name)
        rocksteady = response.body.find(self.rocksteady.name)
        self.assertTrue(footclan < rocksteady < turtles)
        self.assertTrue(turtles < leonardo < raphael)

    def testDescriptionInResponse(self):
        response = self.app.get(reverse('units-list'))
        self.assertTrue(self.leonardo.description in response)
        self.assertTrue(self.raphael.description in response)
        self.assertTrue(self.rocksteady.description in response)
        self.assertTrue(self.april.description not in response)

    def testEmailInResponse(self):
        response = self.app.get(reverse('units-list'))
        self.assertTrue(self.leonardo.email in response)
        self.assertTrue(self.raphael.email in response)
        self.assertTrue(self.rocksteady.email in response)
        self.assertTrue(self.april.email not in response)

    def testTwitterInResponse(self):
        response = self.app.get(reverse('units-list'))
        twitter_url = 'http://twitter.com/{handle}'
        twitter_raphael = twitter_url.format(handle=self.raphael.twitter)
        twitter_rocksteady = twitter_url.format(handle=self.rocksteady.twitter)
        twitter_april = twitter_url.format(handle=self.april.twitter)
        self.assertTrue(twitter_raphael in response)
        self.assertTrue(twitter_rocksteady in response)
        self.assertTrue(twitter_april not in response)

        # Raphael is the last turtle. We assume that the unit list will be
        # where the last occurance of the names come up (so they can crop up
        # in a side bar (this breaks if the side bar is to the right).
        # Leonardo doesn't use Twitter so there shouldn't be a twitter url
        # between the last Leo's name and Raph's name
        leonardo = response.body.rfind(self.leonardo.name)
        raphael = response.body.rfind(self.raphael.name)
        twitter = response.body.find('http://twitter.com/', leonardo, raphael)
        self.assertTrue(twitter == -1)

    def testUrlInResponse(self):
        response = self.app.get(reverse('units-list'))

        self.assertTrue(self.raphael.url in response)
        self.assertTrue(self.rocksteady.url in response)
        self.assertTrue(self.april.url not in response)

        # Raphael is the last turtle. We assume that the unit list will be
        # where the last occurance of the names come up (so they can crop up
        # in a side bar (this breaks if the side bar is to the right).
        # Leonardo doesn't have a website so there shouldn't be a
        # 'Personal website' between the last Leo's name and Raph's name

        leonardo = response.body.rfind(self.leonardo.name)
        raphael = response.body.rfind(self.raphael.name)
        website = response.body.find('Personal website', leonardo, raphael)
        self.assertTrue(website == -1)
