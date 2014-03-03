import datetime

from django.test import TestCase
from django.utils import timezone

from ..models import Job
from ..search_indexes import JobIndex


class JobIndexTest(TestCase):
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

    def test_queryset_includes_open_jobs(self):
        index = JobIndex()

        self.assertIn(self.donkey, index.index_queryset())
        self.assertIn(self.tiger, index.index_queryset())

    def test_queryset_excludes_closed_jobs(self):
        index = JobIndex()

        self.assertNotIn(self.kitten, index.index_queryset())
