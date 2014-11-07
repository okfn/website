from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from ..models import PressMention, PressRelease
from ..search_indexes import PressMentionIndex, PressReleaseIndex


class PressMentionIndexTest(TestCase):
    def setUp(self):  # flake8: noqa
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

    def test_queryset_includes_press_mentions(self):
        index = PressMentionIndex()

        self.assertIn(self.mention, index.index_queryset())
        self.assertNotIn(self.unpublished_mention, index.index_queryset())


class PressReleaseIndexTest(TestCase):
    def setUp(self):  # flake8: noqa
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

    def test_queryset_includes_published_releases(self):
        index = PressReleaseIndex()

        self.assertIn(self.one_month_old, index.index_queryset())
        self.assertIn(self.one_day_old, index.index_queryset())

    def test_queryset_excludes_unpublished_releases(self):
        index = PressReleaseIndex()

        self.assertNotIn(self.in_ten_minutes, index.index_queryset())
