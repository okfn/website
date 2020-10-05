from django.urls import reverse
from django.utils import timezone
from django.template import defaultfilters

from django_webtest import WebTest

from datetime import timedelta

from ..models import PressRelease, PressMention


class PressReleaseViewTest(WebTest):
    def setUp(self):

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

    def test_old_releases_in_response(self):
        response = self.app.get(reverse('press-releases'))
        # Older releases should only have a title and a link
        self.assertTrue(self.one_month_old.title in response)
        self.assertTrue(self.one_month_old.body not in response)

        one_month_old_url = reverse('press-release',
                                    kwargs={'slug': self.one_month_old.slug})
        self.assertTrue(one_month_old_url in response)

        # Newest release should have title, link and body
        self.assertTrue(self.one_day_old.title in response)
        self.assertTrue(self.one_day_old.body in response)
        one_day_old_url = reverse('press-release',
                                  kwargs={'slug': self.one_day_old.slug})
        self.assertTrue(one_day_old_url in response)

        # Newest should be on top
        one_day_ago = response.text.find(self.one_day_old.title)
        one_month_ago = response.text.find(self.one_month_old.title)
        self.assertTrue(one_day_ago < one_month_ago)

    def test_future_releases_not_in_response(self):
        response = self.app.get(reverse('press-releases'))
        self.assertTrue(self.in_ten_minutes.title not in response)

    def test_single_release_response(self):
        response = self.app.get(
            reverse('press-release', kwargs={'slug': self.one_month_old.slug}))

        self.assertTrue(self.one_month_old.title in response)
        self.assertTrue(self.one_month_old.body in response)

        # The title can be present so we look for the body
        self.assertTrue(self.one_day_old.body not in response)

    def test_no_access_to_future_release_response(self):
        response = self.app.get(
            reverse('press-release', kwargs={'slug': self.in_ten_minutes.slug}),
            expect_errors=True)

        self.assertTrue('404' in response.status)

    def test_future_releases_not_in_mentions_response(self):
        response = self.app.get(reverse('press-mentions'))
        self.assertTrue(self.in_ten_minutes.title not in response)


class PressMentionViewTest(WebTest):
    def setUp(self):

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
            publication_date=timezone.now() - timedelta(days=1),
            url='http://www.runwaylive.com/open-fashion',
            title='Open Fashion is the way to go!',
            slug='open-fashion-is-the-new-black',
            author='Andrea Sachs',
            notes='Woo, open fashion!',
            published=False
        )

    def test_press_mention_in_response(self):
        response = self.app.get(reverse('press-mentions'))

        self.assertTrue(self.mention.publisher in response)
        self.assertTrue(self.mention.url in response)
        self.assertTrue(self.mention.title in response)
        self.assertTrue(self.mention.author in response)
        self.assertTrue(self.mention.notes in response)

        date = defaultfilters.date(self.mention.publication_date)
        self.assertTrue(date in response)

        mention_url = reverse('press-mention',
                              kwargs={'slug': self.mention.slug})
        self.assertTrue(mention_url in response)

    def test_press_releases_in_response(self):
        response = self.app.get(reverse('press-mentions'))
        releases_url = reverse('press-releases')
        self.assertTrue(releases_url in response)

    def test_current_press_mention_not_in_mentions_list(self):
        mention_url = reverse('press-mention',
                              kwargs={'slug': self.mention.slug})
        response = self.app.get(mention_url)
        self.assertNotIn(mention_url, response)

    def test_unpublished_mention_not_in_response(self):
        response = self.app.get(reverse('press-mentions'))

        self.assertTrue(self.unpublished_mention.publisher not in response)
        self.assertTrue(self.unpublished_mention.url not in response)
        self.assertTrue(self.unpublished_mention.title not in response)
        self.assertTrue(self.unpublished_mention.author not in response)
        self.assertTrue(self.unpublished_mention.notes not in response)

        date = defaultfilters.date(self.unpublished_mention.publication_date)
        self.assertTrue(date not in response)

        mention_url = reverse('press-mention',
                              kwargs={'slug': self.unpublished_mention.slug})
        self.assertTrue(mention_url not in response)
