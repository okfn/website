import datetime

from django.core.urlresolvers import reverse
from django.test.utils import override_settings
from django.utils import timezone
from django_webtest import WebTest

from ..models import Job


@override_settings(ROOT_URLCONF='foundation.tests.urls')
class JobListViewTest(WebTest):
    def setUp(self):  # flake8: noqa
        now = timezone.now()
        tomorrow = now + datetime.timedelta(days=1)
        tomorrow_plus_1h = now + datetime.timedelta(days=1, hours=1)
        yesterday = now - datetime.timedelta(days=1)

        self.donkey = Job.objects.create(title='Donkey wrangler',
                                         description='<p>Wrangle donkeys.</p>',
                                         submission_email='donkey@example.com',
                                         submission_closes=tomorrow_plus_1h)
        self.tiger = Job.objects.create(title='Tiger stripe painter',
                                        description='<p>Paint tigers.</p>',
                                        submission_email='tiger@example.com',
                                        submission_closes=tomorrow)
        self.kitten = Job.objects.create(title='Kitten herder',
                                         description='<p>Herd kittens</p>',
                                         submission_email='kitten@example.com',
                                         submission_closes=yesterday)

    def test_displays_open_jobs(self):
        response = self.app.get(reverse('jobs-list'))
        self.assertTrue(self.donkey.title in response)
        self.assertTrue(self.tiger.title in response)

    def test_does_not_display_jobs_past_submission(self):
        response = self.app.get(reverse('jobs-list'))
        self.assertTrue(self.kitten.title not in response)

    def test_displays_nearest_deadline_first(self):
        response = self.app.get(reverse('jobs-list'))
        donkey = response.body.find(self.donkey.title)
        tiger = response.body.find(self.tiger.title)
        self.assertTrue(tiger < donkey)
