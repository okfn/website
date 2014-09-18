from datetime import timedelta

from django.utils import timezone
from cms.test_utils.testcases import CMSTestCase

from ..models import PressMention, PressRelease
from ..cms_plugins import RecentPressMentionsPlugin, RecentPressReleasesPlugin


class RecentPressMentionsPluginTest(CMSTestCase):

    def setUp(self):  # flake8: noqa
        super(RecentPressMentionsPluginTest, self).setUp()

        self.mention = PressMention.objects.create(
            publisher='The Two Times Two',
            publication_date=timezone.now(),
            url='http://2x2.news/a-foundation-has-open-knowledge',
            title='Our foundation knows open',
            slug='our-foundation-knows-open',
            author='Rite R. von Nuus',
            notes='We are famous!',
            published=True
            )

        self.unpublished_mention = PressMention.objects.create(
            publisher='Runway',
            publication_date=timezone.now()- timedelta(days=1),
            url='http://www.runwaylive.com/open-fashion',
            title='Open Fashion is the way to go!',
            slug='open-fashion-is-the-new-black',
            author='Andrea Sachs',
            notes='Woo, open fashion!',
            published=False
            )

    def test_mention_rendered(self):
        plug = RecentPressMentionsPlugin()
        mentions = plug.render({}, plug, 'foo')['recent_mentions']['objects']

        self.assertIn(self.mention, mentions)
        self.assertNotIn(self.unpublished_mention, mentions)


class RecentPressReleasesPluginTest(CMSTestCase):

    def setUp(self):  # flake8: noqa
        super(RecentPressReleasesPluginTest, self).setUp()

        now = timezone.now()

        one_month_ago = now - timedelta(days=31)
        self.one_month_old = PressRelease.objects.create(
            title='Data printer',
            slug='ground-breaking-invention',
            body='You can now turn data to real world objects',
            release_date=one_month_ago
            )

        one_day_ago = now - timedelta(days=1)
        self.one_day_old = PressRelease.objects.create(
            title='Open Knowledge solves world hunger!',
            slug='april-fools',
            body='By turning food to data Open Knowledge solves world hunger',
            release_date=one_day_ago
            )

        ten_minutes_from_now = now + timedelta(minutes=10)
        self.in_ten_minutes = PressRelease.objects.create(
            title='Did you believe us',
            slug='okf-fools-everyone',
            body='We are not smart enought to use the printer that way',
            release_date=ten_minutes_from_now
            )

    def test_old_releases_rendered(self):
        plug = RecentPressReleasesPlugin()
        releases = plug.render({}, plug, 'foo')['recent_releases']['objects']

        self.assertIn(self.one_month_old, releases)
        self.assertIn(self.one_day_old, releases)

    def test_future_releases_not_rendered(self):
        plug = RecentPressReleasesPlugin()
        releases = plug.render({}, plug, 'foo')['recent_releases']['objects']

        self.assertNotIn(self.in_ten_minutes, releases)


